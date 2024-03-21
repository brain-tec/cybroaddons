# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Raveena V (odoo@cybrosys.com)
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
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class ForecastAnalysisReportWizard(models.TransientModel):
    _name = 'forecast.analysis.report'
    _description = 'Forecast Analysis Report'

    product_category_id = fields.Many2one(
        'product.category', string="Product Category",
        help="Category of the product")
    parent_category_id = fields.Many2one(
        'product.category', string="Parent Category",
        help="Parent category of product")
    supplier_id = fields.Many2one(
        'product.supplierinfo', string="Supplier",
        help="Supplier/Vendor of the Product.")
    product_brand_id = fields.Many2one('product.brand', string="Product Brand",
                                       help="Brand of the Product.")
    period = fields.Selection([('1week', 'Last 1 week'),
                               ('2week', 'Last 2 weeks'),
                               ('3week', 'Last 3 weeks'),
                               ('1month', 'Last 1 month'),
                               ('2months', 'Last 2 months'),
                               ('3months', 'Last 3 months'),
                               ('6months', 'Last 6 months'),
                               ('12months', 'Last 12 months'),
                               ('24months', 'Last 24 months'),
                               ('36months', 'Last 36 months'),
                               ], string='Duration', required=True,
                              default='3months',
                              help="The duration of the report. 3 months is "
                                   "the default duration")
    location_ids = fields.Many2many('stock.location', string="Locations",
                                    help="Product locations.")
    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.company,
                                 string="Company",
                                 help="Company of the Product belongs to.")
    partner_id = fields.Many2one('res.partner', string="Partner",
                                 help="Related Partner.")

    @api.onchange('parent_category_id')
    def _onchange_parent_category_id(self):
        """This function will return the domain for the field
        product_category_id with respect to the parent_category_id"""
        if self.parent_category_id:
            return {'domain': {
                'product_category_id': [
                    ('parent_id', '=', self.parent_category_id.id)]}}
        return {'domain': {
            'product_category_id': ()}}

    def _compute_date(self):
        """This function will calculate the start_date with respect to the
        period and returns the result"""
        res = datetime.today() + relativedelta(months=-3)
        if self.period == '1week':
            res = datetime.today() + relativedelta(weeks=-1)
        elif self.period == '2week':
            res = datetime.today() + relativedelta(weeks=-2)
        elif self.period == '3week':
            res = datetime.today() + relativedelta(weeks=-3)
        elif self.period == '1month':
            res = datetime.today() + relativedelta(months=-1)
        elif self.period == '6months':
            res = datetime.today() + relativedelta(months=-6)
        elif self.period == '12months':
            res = datetime.today() + relativedelta(months=-12)
        elif self.period == '24months':
            res = datetime.today() + relativedelta(months=-24)
        elif self.period == '36months':
            res = datetime.today() + relativedelta(months=-36)
        elif self.period == '2months':
            res = datetime.today() + relativedelta(months=-2)
        elif self.period == '5months':
            res = datetime.today() + relativedelta(months=-5)
        return res

    def action_print_report(self):
        """This function will generate the report based on the values
        on the report wizard and returns the report."""
        previous_report = self.env['forecast.report'].search([])
        previous_report.unlink() if previous_report else False
        suppliers = self.env['product.supplierinfo'].search(
            [('partner_id', '=', self.partner_id.id)])
        category_ids = []
        if self.parent_category_id:
            # if there is a parent category, the report will be generated based
            # on the product category as the sub-sub categories
            category_ids = self.env['product.category'].search(
                [('parent_id', '=', self.parent_category_id.id)])
            categ_list = category_ids.ids if category_ids else []
            if categ_list:
                for rec in categ_list:
                    sub_category = self.env['product.category'].search(
                        [('parent_id', '=', rec)])
                    for category in sub_category.ids:
                        if category not in categ_list:
                            categ_list.append(category)
                category_ids = self.env['product.category'].browse(categ_list)
        domain = []
        # if both categories are present, it will generate the
        # report based on the product category only
        if self.parent_category_id and self.product_category_id:
            domain += [('categ_id', '=', self.product_category_id.id)]
        elif self.product_category_id and not self.parent_category_id:
            domain += [('categ_id', '=', self.product_category_id.id)]
        elif not self.product_category_id and self.parent_category_id:
            domain += [('categ_id', '=', self.parent_category_id.id)]
        if self.partner_id:
            domain += [('supplier_id', 'in', suppliers.ids)]
        if self.product_brand_id:
            domain += [('product_brand_id', '=', self.product_brand_id.id)]
        products = self.env['product.product'].search(domain)
        product_ids = tuple([product.id for product in products])
        start_date = self._compute_date()
        current_date = datetime.today()
        query = """
               SELECT sum(sl.product_uom_qty) AS product_uom_qty, 
               sl.product_id, sum(sl.qty_invoiced) AS qty_invoiced 
               FROM sale_order_line AS sl
               JOIN sale_order AS so ON sl.order_id = so.id
               WHERE so.state IN ('sale','done')
               AND so.date_order::date >= %s
               AND so.date_order::date <= %s
               AND sl.product_id in %s 
               group by sl.product_id"""
        params = start_date.date(), current_date.date(), \
            product_ids if product_ids else (0, 0, 0, 0)
        self._cr.execute(query, params)
        result = self._cr.dictfetchall()
        locations = self.location_ids
        if not locations:
            locations = self.env['stock.location'].search([
                ('name', '=', 'Stock')])
        for product in products:
            for location in locations:
                warehouse = location.warehouse_id.id
                sold = 0
                for sol_product in result:
                    if sol_product['product_id'] == product.id:
                        sold = sol_product['qty_invoiced']
                available_qty = product.with_context(
                    {'from_date': start_date, 'to_date': current_date,
                     'warehouse': warehouse}).qty_available
                forecasted_qty = product.with_context(
                    {'warehouse': warehouse}).virtual_available
                reorder_qty = self.env['stock.warehouse.orderpoint'].search(
                    [('product_id', '=', product.id),
                     ('location_id', '=', product.id)])
                reorder_min = sum(
                    [q.product_min_qty for q in reorder_qty])
                minimum_qty = 0
                if available_qty < reorder_min:
                    minimum_qty = reorder_min
                pending = product.with_context(
                    {'from_date': start_date, 'to_date': current_date,
                     'location': location.id}).incoming_qty
                suggested = sold - (forecasted_qty + pending + minimum_qty)
                vals = {
                    'sold': sold,
                    'product_id': product.id,
                    'product_category_id': product.categ_id.id,
                    'supplier_id': product.seller_ids.ids[
                        0] if product.seller_ids else False,
                    'product_brand_id': product.product_brand_id.id,
                    'on_hand': available_qty,
                    'pending': pending,
                    'minimum': minimum_qty,
                    'suggested': suggested,
                    'forecast': forecasted_qty,
                    'location_id': location.id
                }
                self.env['forecast.report'].create(vals)
        return {
            'name': 'Forecast Analysis Report',
            'res_model': 'forecast.report',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'views': [(self.env.ref('inventory_forecast_analysis_report.'
                                    'forecast_report_view_tree'
                                    ).id, 'tree'),
                      (False, 'form'),
                      (self.env.ref('inventory_forecast_analysis_report.'
                                    'forecast_report_view_pivot').id,
                       'pivot')],
            'target': 'current',
        }
