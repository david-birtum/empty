# -*- coding: utf-8 -*-

from odoo import models, fields, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_training_sale = fields.Boolean(
        string='Is training sale?',
        copy=False,
        help='Enables the order to be treated as training.',
    )

    def _get_training_journal(self):
        try:
            return self.env.ref('b_account_training.training_journal')
        except Exception:
            journal_id = self.env['account.journal'].search([
                ('type','=','sale'),
                ('is_training_journal','=',True)
            ], limit=1)
            if not journal_id:
                raise ValidationError(_("There must be at least a Training sale journal set up."))
            return journal_id

    def _create_invoices(self, grouped=False, final=False, date=None):
        training_sales = self.filtered(lambda s:s.is_training_sale)
        if not training_sales:
            return super(SaleOrder, self)._create_invoices(grouped=False, final=final, date=date)
        if training_sales and self != training_sales:
            raise ValidationError(_("Cannot create training and regular invoices together."))
        moves = super(SaleOrder, self)._create_invoices(grouped=True, final=final, date=date)
        for move in moves:
            move.write({
                'is_training_invoice': True,
                'journal_id': self._get_training_journal().id,
                'is_training_readonly': True
            })
        return moves
    