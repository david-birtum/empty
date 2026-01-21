#########################################################
# Module written to Odoo, Open Source Management Solution
#
# Copyright (c) 2024 Birtum - https://www.birtum.com
# All Rights Reserved.
#
# Developer(s): Omar Gómez Cruz - ogc@birtum.com
#               Joanner Paz Martínez - jpm@birtum.com
#########################################################
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################
{
    'name': 'BIRTUM | Account Training',

    'summary': """
        This module adds the next features:
            - 
    """,
    'description': """
        Account Training
    """,

    'author': 'BIRTUM ©',
    'website': 'https://www.birtum.com',

    "category": "Account",
    'version': '18.0.1.0',
    'last_update': '13-08-2025',

    'depends': [
        'account',
        'account_edi',
        'account_reports',
        'purchase',
        'sale',
    ],
    'data': [
        # DATA
        'data/journal_data.xml',
        # SECURITY
        'security/res_groups.xml',
        # VIEWS
        'views/account_journal_views.xml',
        'views/account_move_views.xml',
        'views/account_payment_views.xml',
        'views/account_report_views.xml',
        'views/purchase_order_views.xml',
        'views/sale_order_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'b_account_training/static/src/components/account_reports/filter_extra_options.xml'
        ],
    },

    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
