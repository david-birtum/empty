# -*- coding: utf-8 -*-

from odoo import models, _
from odoo.exceptions import UserError


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    def _create_payments(self):
        payments = super(AccountPaymentRegister, self)._create_payments()
        for payment in payments:
            if payment.reconciled_invoice_ids or payment.reconciled_bill_ids:
                payment.is_training_payment = (payment.reconciled_invoice_ids and all(payment.reconciled_invoice_ids.mapped('is_training_invoice'))) \
                    or (payment.reconciled_bill_ids and all(payment.reconciled_bill_ids.mapped('is_training_invoice')))
        return payments

    def action_create_payments(self):
        if self._context.get('active_model') not in ['account.move', 'account.move.line']:
            raise UserError(_(
                "The register payment wizard should only be called on account.move or account.move.line records."
            ))

        return super(AccountPaymentRegister, self).action_create_payments()