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
from odoo import models


class ProjectProject(models.Model):
    """ Fetch Project Records """
    _inherit = 'project.project'

    def project_records(self):
        """ Fetch all project details """
        projects = self.search_read([], ['id', 'name'])
        return projects


class ProjectTask(models.Model):
    """ Fetch task records """
    _inherit = 'project.task'

    def task_records(self):
        """ Fetch all task details """
        tasks = self.search_read([], ['id', 'name'])
        return tasks
