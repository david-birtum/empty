from odoo import fields, models, api


class SaleReport(models.Model):
    _inherit = 'sale.report'

    is_training_sale = fields.Boolean(
        string='Is training sale?',
        copy=False,
        help='Enables the order to be treated as training.',
    )

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res['is_training_sale'] = "s.is_training_sale"
        return res
