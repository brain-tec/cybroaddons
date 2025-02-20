# -*- coding: utf-8 -*-
###############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2025-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Aysha Shalin (odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC
#    LICENSE (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
import logging
from odoo import models, api

_logger = logging.getLogger(__name__)


class DuplicateRecord(models.TransientModel):
    """ Created model to duplicate the record """
    _name = 'duplicate.record'
    _description = 'Duplicate Records'

    @api.model
    def action_duplicate_records(self, selected_values):
        """ Duplicating the records.
        params: dict selected_values: list of records of selected One2many fields.
        """
        values = selected_values.get('values')
        model = selected_values.get('model')

        _logger.info(f"Model: {model}, Values: {values}")

        if values and isinstance(values, (list, int)):
            try:
                record = self.env[model].browse(values)
                if not record.exists():
                    _logger.info(
                        "No valid records found for the provided values.")
                    return True

                for rec in record:
                    datas = list(rec.read())  # This reads the record data
                    for data in datas[0]:
                        is_tuple = isinstance(datas[0][data], tuple)
                        if is_tuple:
                            datas[0][data] = datas[0][data][0]
                    self.env[model].create(datas)
            except Exception as e:
                _logger.error(f"An error occurred: {e}")
        else:
            _logger.info(
                "Invalid or missing 'values' or 'model'. Skipping execution.")
        return True
