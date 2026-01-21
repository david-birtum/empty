# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    is_training_invoice = fields.Boolean(
        string='Is training invoice?', 
        related='move_id.is_training_invoice',
        store=True
    )