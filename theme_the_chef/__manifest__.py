# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2020-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
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
    'name': 'The Chef Theme',
    'description': 'The Chef Theme',
    'version': '14.0.1.0.0',
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'category': 'Theme/Corporate',
    'depends': ['website'],
    'data': [
        'views/assets.xml',
        'views/layout.xml',
        'views/templates.xml',
        'views/snippets/about.xml',
        'views/snippets/banner.xml',
        'views/snippets/branches.xml',
        'views/snippets/happy.xml',
        'views/snippets/menu.xml',
        'views/snippets/reservation.xml',
        'views/snippets/special.xml',
        'views/snippets/special_left.xml',
        'views/snippets/team.xml',
    ],
    'license': 'LGPL-3',
    'images': [
        'static/description/banner.jpg',
        'static/description/theme_screenshot.jpg',
    ],
    'installable': True,
    'application': True,
}
