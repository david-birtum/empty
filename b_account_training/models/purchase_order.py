# -*- coding: utf-8 -*-

from odoo import fields, models, _
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    is_training_purchase = fields.Boolean(
        string='Is training purchase?',
        copy=False,
        help='Enables the order to be treated as training.',
    )

    def _get_training_journal(self):
        try:
            return self.env.ref('b_account_training.training_vendor_journal')
        except Exception:
            journal_id = self.env['account.journal'].search([
                ('type', '=', 'purchase'),
                ('is_training_journal', '=', True)
            ], limit=1)
            if not journal_id:
                raise ValidationError(_("There must be at least a Training purchase journal set up."))
            return journal_id

    def _prepare_invoice(self):
        res = super(PurchaseOrder, self)._prepare_invoice()
        if self.is_training_purchase:
            res.update({
                'is_training_invoice': True,
                'journal_id': self._get_training_journal().id,
                'is_training_readonly': True
            })
        return res