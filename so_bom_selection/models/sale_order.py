# -*- coding: utf-8 -*-
################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Cybrosys Techno Solutions(odoo@cybrosys.com)
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
from odoo import models


class SaleOrder(models.Model):
    """Inherited model 'sale.order'"""
    _inherit = 'sale.order'

    def action_confirm(self):
        """ Create manufacturing order of components in selected BOM """
        for rec in self.order_line:
            if rec.bom_id and rec.bom_id in rec.product_template_id.bom_ids:
                # Store the original sequence order
                original_sequences = {bom.id: bom.sequence for bom in rec.product_template_id.bom_ids}
                # Set the selected BOM's sequence to 0
                rec.bom_id.sequence = 0
                # Get all other BOMs and update their sequence accordingly
                other_boms = rec.product_template_id.bom_ids - rec.bom_id
                sequence_counter = 1  # Start sequence from 1 for others
                for bom in other_boms.sorted('sequence'):
                    bom.sequence = sequence_counter
                    sequence_counter += 1
        result = super().action_confirm()
        # Restore original sequences after the confirmation
        for rec in self.order_line:
            if rec.bom_id and rec.bom_id in rec.product_template_id.bom_ids:
                for bom in rec.product_template_id.bom_ids:
                    if bom.id in original_sequences:
                        bom.sequence = original_sequences[bom.id]
            manufacturing_order = self.env["mrp.production"].search(
                [('origin', '=', self.name),
                 ('state', '=', 'confirmed')])
            if manufacturing_order:
                for mo in manufacturing_order:
                    print(mo.product_qty)
                    mo.update({'qty_to_produce': mo.product_qty})
                # mo.update({'state':'draft'})
        return result

    def write(self, values):
        """Super write method to change the qty_to_produce in the MO
            based on sale order quantity"""
        res = super().write(values)
        for order_line in self.order_line:
            if order_line.product_uom_qty:
                manufacturing_order = self.env["mrp.production"].search(
                    [('origin', '=', self.name),
                     ('state', '=', 'confirmed')])
                if manufacturing_order:
                    for mo in manufacturing_order:
                        mo.write({'qty_to_produce': mo.product_qty})
        return res

