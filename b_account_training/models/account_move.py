# -*- coding: utf-8 -*-
import logging
from collections import defaultdict

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError, UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    is_training_invoice = fields.Boolean(
        string='Is training invoice/entry?', 
        copy=False,
    )
    is_training_readonly = fields.Boolean(
        string='Is training readonly?',
        readonly=True,
        copy=False)

    def _search_default_journal(self):
        # Odoo 18.0: payment_id ya no existe en account.move, se movió a otras estructuras
        # Verificar campos solo si existen en el modelo
        if hasattr(self, 'payment_id') and self.payment_id and self.payment_id.journal_id:
            return self.payment_id.journal_id
        if hasattr(self, 'statement_line_id') and self.statement_line_id and self.statement_line_id.journal_id:
            return self.statement_line_id.journal_id
        if hasattr(self, 'statement_line_ids') and self.statement_line_ids and self.statement_line_ids.statement_id.journal_id:
            return self.statement_line_ids.statement_id.journal_id[:1]

        journal_types = self._get_valid_journal_types()
        company = self.company_id or self.env.company
        domain = [
            *self.env['account.journal']._check_company_domain(company),
            ('type', 'in', journal_types),
            ('is_training_journal', '=', self.is_training_invoice),
        ]

        journal = None
        # the currency is not a hard dependence, it triggers via manual add_to_compute
        # avoid computing the currency before all it's dependences are set (like the journal...)
        if self.env.cache.contains(self, self._fields['currency_id']):
            currency_id = self.currency_id.id or self._context.get('default_currency_id')
            if currency_id and currency_id != company.currency_id.id:
                currency_domain = domain + [('currency_id', '=', currency_id)]
                journal = self.env['account.journal'].search(currency_domain, limit=1)

        if not journal:
            journal = self.env['account.journal'].search(domain, limit=1)

        if not journal:
            error_msg = _(
                "No journal could be found in company %(company_name)s for any of those types: %(journal_types)s",
                company_name=company.display_name,
                journal_types=', '.join(journal_types),
            )
            raise UserError(error_msg)

        return journal

    @api.depends('company_id', 'invoice_filter_type_domain', 'is_training_invoice')
    def _compute_suitable_journal_ids(self):
        super()._compute_suitable_journal_ids()
        for move in self:
            move.suitable_journal_ids = move.suitable_journal_ids.filtered(
                lambda journal: journal.is_training_journal == move.is_training_invoice
            )

    @api.depends('move_type', 'is_training_invoice')
    def _compute_journal_id(self):
        training_moves = self.filtered(lambda move: move.is_training_invoice)
        training_moves_to_update_journal = training_moves.filtered(
            lambda move: not move.journal_id.is_training_journal
        )
        other_moves = self - training_moves
        other_moves.filtered(lambda move: move.journal_id.is_training_journal).write(dict(journal_id=False))

        if training_moves:
            moves_by_type = defaultdict(lambda: self.env['account.move'])
            for move in training_moves:
                moves_by_type[move.invoice_filter_type_domain or 'general'] |= move

            for journal_type, training_moves in moves_by_type.items():
                training_journals = self.env['account.journal'].search([
                    *self.env['account.journal']._check_company_domain(self.env.company),
                    ('type', '=', journal_type),
                    ('is_training_journal', '=', True),
                ])
                if training_moves_to_update_journal and not training_journals:
                    raise ValidationError(_("There must be at least a Training sale journal set up."))
                if training_moves_to_update_journal:
                    training_moves_to_update_journal.write(dict(journal_id=training_journals[0].id))

        super(AccountMove, other_moves)._compute_journal_id()

    def action_post(self):
        if not self.env.context.get('is_training', False):
            for move in self:
                if move.is_training_invoice and not move.journal_id.is_training_journal:
                    raise ValidationError(_("All training invoices must have a training journal selected."))
                elif not move.is_training_invoice and move.journal_id.is_training_journal:
                    raise ValidationError(_("Regular invoices cannot have a training journal selected."))
        return super(AccountMove, self).action_post()

    @api.model_create_multi
    def create(self, vals_list):
        if isinstance(vals_list, list):
            for val in vals_list:
                journal_id = val.get('journal_id', False)
                journal = self.env['account.journal'].browse(journal_id) if journal_id else self.env['account.journal']
                if ((not val.get('is_training_invoice', False) and self.env.context.get('is_training', False)) or
                        (journal and journal.is_training_journal)):
                    val.update(dict(is_training_invoice=True))
        else:
            if not vals_list.get('is_training_invoice', False) and self.env.context.get('is_training', False):
                vals_list.update(dict(is_training_invoice=True))

        res = super().create(vals_list=vals_list)
        return res

    def action_register_payment(self):
        res = super().action_register_payment()
        all_training_invoices = all(self.mapped('is_training_invoice'))
        if all_training_invoices:
            res['context']['default_is_training_payment'] = all_training_invoices
            res['context']['is_training'] = all_training_invoices
        return res

    def update_tr(self):
        _logger = logging.getLogger(__name__)
        env = self.env
        log = _logger.info

        log("*********************************************")

        morgan_account_moves = env['account.move'].sudo().search([('name', 'ilike', 'FT-00001-%')])
        log("FACTURAS:%s" % len(morgan_account_moves))
        if morgan_account_moves:

            moves_query = "UPDATE account_move SET is_training_invoice = True WHERE id in %s"
            moves_params = (tuple(morgan_account_moves.ids),)
            env.cr.execute(moves_query, moves_params)

            move_lines_query = "UPDATE account_move_line SET is_training_invoice = True WHERE move_id in %s"
            move_lines_params = (tuple(morgan_account_moves.ids),)
            env.cr.execute(move_lines_query, move_lines_params)

            morgan_sales = morgan_account_moves.mapped('line_ids.sale_line_ids.order_id')
            log("VENTAS:%s" % len(morgan_sales))
            if morgan_sales:
                morgan_sales.write(dict(is_training_sale=True))

        morgan_payments = env['account.payment'].sudo().search([]).filtered(
            lambda move: any(
                move.reconciled_invoice_ids.mapped('is_training_invoice') + move.reconciled_bill_ids.mapped(
                    'is_training_invoice'))
        )
        log("PAGOS:%s" % len(morgan_payments))
        if morgan_payments:
            payments_query = "UPDATE account_payment SET is_training_payment = True WHERE id in %s"
            payments_params = (tuple(morgan_payments.ids),)
            env.cr.execute(payments_query, payments_params)
        log("*********************************************")

        log("*********************************************")

        morgan_payments = env['account.payment'].sudo().search([('is_training_payment', '=', True)])
        log("Payments:%s" % len(morgan_payments))

        morgan_moves = morgan_payments.mapped('move_id').filtered(lambda move: not move.is_training_invoice)
        log("MOVES:%s" % len(morgan_moves))
        if morgan_moves:
            moves_query = "UPDATE account_move SET is_training_invoice = True WHERE id in %s"
            moves_params = (tuple(morgan_moves.ids),)
            env.cr.execute(moves_query, moves_params)

        morgan_moves = env['account.move'].sudo().search([('is_training_invoice', '=', True)])
        if morgan_moves:
            morgan_move_lines = morgan_moves.mapped('line_ids')
            if morgan_move_lines:
                log("MOVES LINES: %s" % len(morgan_move_lines))
                moves_query = "UPDATE account_move_line SET is_training_invoice = True WHERE id in %s"
                moves_params = (tuple(morgan_move_lines.ids),)
                env.cr.execute(moves_query, moves_params)

        log("*********************************************")