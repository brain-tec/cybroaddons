# -*- coding: utf-8 -*-
################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: MOHAMMED DILSHAD TK (odoo@cybrosys.com)
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
################################################################################
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class EventServiceLine(models.Model):
    """Model to manage the service lines of the event management"""
    _name = 'event.service.line'
    _description = 'Event Service Line'

    service = fields.Selection([('', '')], string="Services",
                               required=True, help="Name of service")
    event_id = fields.Many2one('event.management', string="Event",
                               help="Name of the events")
    date_from = fields.Datetime(string="Date from", required=True,
                                help="Start date of service")
    date_to = fields.Datetime(string="Date to", required=True,
                              help="End date of the service")
    amount = fields.Float(string="Amount", readonly=True, help="Total amount "
                                                               "of a service")
    state = fields.Selection([('done', 'Done'), ('pending', 'Pending')],
                             string="State", default="pending",
                             readonly=True, help="Stages of the events")
    currency_id = fields.Many2one('res.currency', readonly=True,
                                  default=lambda self:
                                  self.env.user.company_id.currency_id,
                                  help="Currency of current company",
                                  string="Currency")
    invoiced = fields.Boolean(string="Invoiced", readonly=True,
                              help="Is this service invoiced")
    related_product_id = fields.Many2one('product.product',
                                         string="Related Product",
                                         help="List of related Products")
    _sql_constraints = [('event_supplier_unique', 'unique(event_id, service)',
                         'Duplication Of Service In The Service Lines '
                         'Is not Allowed')]

    @api.constrains('date_from', 'date_to')
    def _check_date_to_date_from(self):
        """ Checking is end date less than start date"""
        for rec in self:
            if rec.date_to < rec.date_from:
                raise ValidationError(_("Date to cannot be set before "
                                        "`Date from` Check the 'Date from' and "
                                        "'Date to' of the '%s' service"
                                        % rec.service))
