from odoo import fields, models, api


class PurchaseReport(models.Model):
    _inherit = 'purchase.report'

    is_training_purchase = fields.Boolean(
        string='Is training purchase?',
        copy=False,
        help='Enables the order to be treated as training.',
    )

    def _select(self):
        from odoo.tools import SQL
        res = super()._select()
        return SQL("%s, po.is_training_purchase", res)
