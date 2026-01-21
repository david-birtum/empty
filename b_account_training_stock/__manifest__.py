#########################################################
# Module written to Odoo, Open Source Management Solution
#
# Copyright (c) 2022 Birtum - https://www.birtum.com
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
    'name': 'BIRTUM | Account Training Stock',
    'summary': """This module adds performance training for Stock""",
    'description': """Account Training Stock""",
    'author': 'BIRTUM ©',
    'website': 'https://www.birtum.com',
    "category": "Stock",
    'version': '18.0.0.1',
    'last_update': '05-07-2024',
    'depends': [
        'b_account_training',
        'stock_account'
    ],
    'data': [
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
