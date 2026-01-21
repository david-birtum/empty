# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    is_training_journal = fields.Boolean(string='Is training journal?')
    