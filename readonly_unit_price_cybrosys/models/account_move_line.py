# -*- coding: utf-8 -*-
#############################################################################
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
#############################################################################
from odoo import fields, models


class AccountMoveLine(models.Model):
    """Inherits the model for adding readonly field and function."""
    _inherit = 'account.move.line'

    price_unit_boolean = fields.Boolean(
        string="Price Unit Boolean",
        help="This field used to readonly for price unit",
        default=lambda self: self.env.user.readonly_unit_price_invoicing,
        compute='_compute_price_unit_boolean')

    def _compute_price_unit_boolean(self):
        """ Compute function for price_unit_boolean.
               This function will check the boolean field  of the currently
               logged user is true or false.
               And it will pass the value to price_unit_boolean."""
        for rec in self:
            rec.price_unit_boolean = self.env.user.readonly_unit_price_invoicing
