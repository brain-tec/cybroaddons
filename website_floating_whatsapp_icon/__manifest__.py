# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2025-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions (odoo@cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
{
    'name': "WhatsApp Floating Icon in Website",
    'version': '18.0.1.0.0',
    'category': 'Extra Tools',
    'summary': """Adds a WhatsApp Floating Icon in Website to connect with
    WhatsApp web.""",
    'description': """A WhatsApp icon is added to the website pages, allowing 
    users to easily access WhatsApp Web with a single click. When clicked, the
    icon redirects users to WhatsApp Web.""",
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'website': "https://www.cybrosys.com",
    'depends': ['base','website'],
    'data': [
        'views/website_views.xml',
        'views/website_whatsapp_icons_views.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            '/website_floating_whatsapp_icon/static/src/css/website_floating_whatsapp_icon.css',
        ],
    },
    'images': ['static/description/banner.png'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
