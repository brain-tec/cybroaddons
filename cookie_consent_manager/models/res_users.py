# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C)2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Rosmy John@cybrosys(odoo@cybrosys.com)
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
#
#############################################################################
from odoo import fields, models


class ResUsers(models.Model):
    """ Extend the 'res.users' model to add a field indicating whether cookies
    are enabled for a user. """
    _inherit = 'res.users'

    cookies_enabled = fields.Boolean(string='Cookies Enabled',
                                     help='Indicates whether cookies are '
                                          'enabled for this user.')
