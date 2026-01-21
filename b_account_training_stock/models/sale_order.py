# -*- coding: utf-8 -*-

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        self = self.with_context(dict(is_training=self.is_training_sale))
        res = super(SaleOrder, self).action_confirm()
        return res
