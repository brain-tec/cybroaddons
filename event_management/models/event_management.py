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
from odoo.exceptions import UserError, ValidationError


class EventManagement(models.Model):
    """Model for managing Event Management"""
    _name = 'event.management'
    _description = 'Event Management'

    name = fields.Char(string="Name", readonly=True, copy=False,
                       help="Name of the event management")
    ref = fields.Char(string="Ref", readonly=True, help="Event Management "
                                                        "Reference")
    type_of_event_id = fields.Many2one('event.management.type',
                                       string="Type",
                                       required=True, help="Type of the event")
    partner_id = fields.Many2one('res.partner', string="Customer",
                                 required=True, help="Client")
    date = fields.Date(string="Date", default=fields.Date.today, required=True,
                       help="Current Date")
    start_date = fields.Datetime(string="Start date",
                                 default=lambda self: fields.datetime.now(),
                                 required=True, help="Start date of the event"
                                                     " management")
    end_date = fields.Datetime(string="End date", required=True,
                               help="End date of the event management")
    service_line_ids = fields.One2many(comodel_name='event.service.line',
                                       inverse_name='event_id',
                                       string="Services",
                                       help="Services of the event. "
                                            "Automatically adds when "
                                            "service modules are downloaded.")
    state = fields.Selection(selection=
        [('draft', 'Draft'), ('confirm', 'Confirmed'),
         ('invoice', 'Invoiced'), ('close', 'Close'), ('cancel', 'Canceled')],
        string="State", default="draft", help="stages of"
                                              " the event")
    note = fields.Text(string="Terms and conditions", help="Note for the event")
    price_subtotal = fields.Float(string='Total',
                                  compute='_compute_price_subtotal', store=True,
                                  help="Sub total price")
    image = fields.Binary(string="Image", attachment=True,
                          help="This field holds the image used as image for "
                               "the event, limited to 1080x720px.")
    currency_id = fields.Many2one(comodel_name='res.currency', readonly=True,
                                  default=lambda self:
                                  self.env.user.company_id.currency_id,
                                  help="Default currency is currency of the "
                                       "company", string="Currency")
    invoice_count = fields.Integer(string="Invoice Count", help="Count of "
                                                                "the invoices")
    invoice_ids = fields.Many2many(comodel_name="account.move", copy=False,
                                   string="Invoices", help="Corresponding "
                                                           "invoices")
    pending_invoice = fields.Boolean(string="Invoice Pending",
                                     compute='_compute_pending_invoice',
                                     help="Is invoice Pending")

    @api.depends('service_line_ids', 'service_line_ids.state')
    def _compute_pending_invoice(self):
        """Computes the  invoices"""
        self.pending_invoice = any(
            line.state == 'done' and not line.invoiced for line in
            self.service_line_ids)

    @api.depends('service_line_ids', 'service_line_ids.amount')
    def _compute_price_subtotal(self):
        """ Computes price total """
        total = 0
        for items in self.service_line_ids:
            total += items.amount
        self.price_subtotal = total

    @api.model
    def create(self, values):
        """Create method for sequencing and checking dates while creating"""
        if values['start_date'] >= values['end_date']:
            raise UserError(_('Start date must be less  than End date'))
        name = f"%s-%s-%s" % (
            self.env['res.partner'].browse(values['partner_id']
                                           ).name,
            self.env['event.management.type'].browse(
                values['type_of_event_id']).name, values['date'])
        values['name'] = name
        values['ref'] = self.env['ir.sequence'].next_by_code(
            'event.order.sequence')
        return super(EventManagement, self).create(values)

    def action_event_confirm(self):
        """Button action to confirm"""
        self.state = "confirm"

    def action_event_cancel(self):
        """Button action to cancel"""
        self.state = "cancel"

    def action_event_close(self):
        """Button action to close"""
        pending = 0
        for lines in self.service_line_ids:
            if lines.invoiced is False:
                pending = 1
        if pending == 1:
            raise ValidationError(_('You can close an event only when all '
                                    'services is Done and Invoiced'))
        self.state = "close"

    def action_view_invoice_event(self):
        """Button action to View the related invoice"""
        invoices = self.mapped('invoice_ids')
        action = self.env.ref('account.action_move_out_invoice_type'
                              ).sudo().read()[0]
        if len(invoices) > 1:
            action['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            action['views'] = [
                (self.env.ref('account.view_move_form').id, 'form')]
            action['res_id'] = invoices.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    def action_event_invoice_create(self):
        """Button action to create related invoice"""
        product_line = []
        payment_list = []
        for line in self.service_line_ids:
            if line.invoiced is False and line.state == "done":
                product_line.append({'product_id': line.related_product_id,
                                     'price_unit': line.amount})
                line.invoiced = True
        if len(product_line) > 0:
            partner = self.partner_id
            for records in product_line:
                product_id = records['product_id']
                if product_id.property_account_income_id.id:
                    income_account = product_id.property_account_income_id.id
                elif product_id.categ_id.property_account_income_categ_id.id:
                    income_account = product_id.categ_id. \
                        property_account_income_categ_id.id
                else:
                    raise UserError(
                        _('Please define income account for'
                          ' this product: "%s" (id:%d).') % (
                            product_id.name, product_id.id))
                inv_line_data = {
                    'name': self.name,
                    'account_id': income_account,
                    'price_unit': records['price_unit'],
                    'quantity': 1,
                    'product_id': product_id.id,
                    'product_uom_id': product_id.uom_id.id,
                }
                payment_list.append((0, 0, inv_line_data))
            inv_data = {
                'move_type': 'out_invoice',
                'ref': self.name,
                'bank_partner_id': partner.property_account_payable_id.id,
                'partner_id': partner.id,
                'payment_reference': self.name,
                'company_id': self.env.user.company_id.id,
                'invoice_line_ids': payment_list,
            }
            inv_id = self.env['account.move'].create(inv_data)
            result = {
                'view_type': 'form',
                'res_model': 'account.move',
                'res_id': inv_id.id,
                'view_id': False,
                'view_mode': 'form',
                'type': 'ir.actions.act_window'
            }
            self.state = "invoice"
            all_invoice_ids = self.invoice_ids.ids
            all_invoice_ids.append(inv_id.id)
            self.update({'invoice_ids': all_invoice_ids,
                         'invoice_count': self.invoice_count + 1})
            return result
