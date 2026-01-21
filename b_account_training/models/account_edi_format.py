# -*- coding: utf-8 -*-

from odoo import models


class AccountEdiFormat(models.Model):
    _inherit = 'account.edi.format'

    def _get_move_applicability(self, move):
        # EXTENDS account_edi
        self.ensure_one()
        if move.is_training_invoice:
            return None
        return super()._get_move_applicability(move)

