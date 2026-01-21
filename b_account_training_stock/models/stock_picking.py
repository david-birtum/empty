# -*- coding: utf-8 -*-

from odoo import fields, models, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    is_training = fields.Boolean(
        string="Is training picking"
    )

    def _prepare_picking_vals(self, partner, picking_type, location_id, location_dest_id):
        res = super()._prepare_picking_vals(partner, picking_type, location_id, location_dest_id)
        res.update(dict(is_training=self.env.context.get('is_training', False)))
        return res

    @api.model_create_multi
    def create(self, vals_list):
        if self.env.context.get('is_training', False):
            for val in vals_list:
                val.update(dict(is_training=self.env.context.get('is_training', False)))
        return super().create(vals_list)
