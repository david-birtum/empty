# -*- coding: utf-8 -*-

from odoo import api, models, fields


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    is_training_payment = fields.Boolean(string='Is training payment?')

    @api.depends('payment_type', 'is_training_payment')
    def _compute_available_journal_ids(self):
        """
        Get all journals having at least one payment method for inbound/outbound depending on the payment_type.
        """
        journals = self.env['account.journal'].search([
            '|',
            ('company_id', 'parent_of', self.env.company.id),
            ('company_id', 'child_of', self.env.company.id),
            ('type', 'in', ('bank', 'cash')),
        ])
        for pay in self:
            if pay.payment_type == 'inbound':
                pay.available_journal_ids = journals.filtered(
                    lambda journal: journal.inbound_payment_method_line_ids and
                                    journal.is_training_journal == pay.is_training_payment
                )
            else:
                pay.available_journal_ids = journals.filtered(
                    lambda journal: journal.outbound_payment_method_line_ids and
                                    journal.is_training_journal == pay.is_training_payment
                )

    @api.model_create_multi
    def create(self, vals_list):
        is_training = self.env.context.get('is_training', False)
        if is_training:
            for val in vals_list:
                val.update(dict(is_training_payment=is_training))
        payments = super(AccountPayment, self).create(vals_list)

        if is_training:
            moves = payments.filtered(lambda payment: payment.move_id)
            moves.write(dict(is_training_invoice=is_training))

        return payments

    def write(self, vals):
        res = super().write(vals)

        if 'is_training_payment' in vals:
            for payment in self:
                if payment.move_id:
                    payment.move_id.is_training_invoice = payment.is_training_payment

        return res

    @api.returns('self')
    def copy_multi(self, default=None):
        res = super(AccountPayment, self).copy_multi(default)
        return res
