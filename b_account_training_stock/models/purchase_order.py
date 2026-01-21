# -*- coding: utf-8 -*-

from odoo import models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def _create_picking(self):
        self = self.with_context(dict(is_training=self.is_training_purchase))
        return super(PurchaseOrder, self)._create_picking()
