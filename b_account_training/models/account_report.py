# -*- coding: utf-8 -*-

from odoo import api, models, fields


class AccountReport(models.Model):
    _inherit = 'account.report'

    filter_show_training = fields.Boolean(
        string="Training Entries",
        compute=lambda x: x._compute_report_option_filter('filter_show_training', True),
        readonly=False,
        store=True,
        depends=['root_report_id'],
    )

    def get_report_information(self, options):
        info = super().get_report_information(options)
        info['filters']['training_entries'] = self.filter_show_training
        return info

    ####################################################
    # OPTIONS: TRAINING ENTRIES
    ####################################################
    def _init_options_training_entries(self, options, previous_options=None):
        if self.filter_show_training and previous_options:
            options['training_entries'] = previous_options.get('training_entries', False)
        else:
            options['training_entries'] = False

    @api.model
    def _get_options_training_entries_domain(self, options):
        if not options.get('training_entries'):
            return [('is_training_invoice', '=', False)]
        else:
            return []

    ####################################################
    # OPTIONS: CORE
    ####################################################
    @api.model
    def _get_options_domain(self, options, date_scope):
        domain = super(AccountReport, self)._get_options_domain(options, date_scope)
        domain += self._get_options_training_entries_domain(options)
        return domain