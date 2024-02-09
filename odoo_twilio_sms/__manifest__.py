# -*- coding: utf-8 -*-
################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Busthana Shirin (odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
################################################################################
{
    'name': 'Twilio SMS Gateway',
    'version': '15.0.1.0.0',
    'category': 'Extra Tools',
    'summary': """Send SmS through twilio""",
    'description': """The module helps to send SmS through twilio""",
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'website': 'https://www.cybrosys.com',
    'depends': ['base_setup', 'sale', 'purchase', 'base'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron_data.xml',
        'views/purchase_order_views.xml',
        'views/sale_order_views.xml',
        'views/twilio_account_views.xml',
        'views/twilio_sms_group_views.xml',
        'views/twilio_sms_template_views.xml',
        'views/twilio_sms_views.xml',
        'wizard/twilio_sms_interaction_views.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
