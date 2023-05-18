# -*- coding: utf-8 -*-
##############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
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
##############################################################################
import json

from odoo import http
from odoo.http import request


class LoginPage(http.Controller):
    """Controller for the login page. This controller provides methods for
    retrieving the active theme's main color, view font color, and theme font
    color and updating the theme of the login page.
    """
    @http.route(['/active_theme'], auth='public', type='http')
    def find_active_theme(self):
        """find the active theme for updating theme of login page"""
        active_theme = request.env['theme.config'].sudo().search_read(
            domain=[('theme_active', '=', True)],
            fields=['theme_main_color',
                    'view_font_color',
                    'theme_font_color'])
        active_theme = active_theme[0] if active_theme else []
        return json.dumps(active_theme)
