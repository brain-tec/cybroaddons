""" Website custom contact Us"""
# -*- coding: utf-8 -*-
################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2025-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Anzil K A (odoo@cybrosys.com)
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
from odoo import fields, models


class Website(models.Model):
    """  Inherit Website and Adding the necessary fields for Website
    contact us"""
    _inherit = 'website'

    company = fields.Boolean("Company Name", help='If it is true it will'
                                                  'show company name on website')
    address = fields.Boolean("Address", help='If it is true it will '
                                             'show address on website')
    phone = fields.Boolean("Phone", help='If it is true it will show'
                                         ' phone number on website')
    mobile = fields.Boolean("Mobile", help='If it is true it will show mobile '
                                           'number on website')
    email = fields.Boolean("Email", help='If it is true it will show email '
                                         'on website')
    website = fields.Boolean("Website", help='If it is true it will show '
                                             'website name on website')
    vat = fields.Boolean("VAT", help='If it is true it will show tax id '
                                     'on website')
    address_in_online = fields.Boolean("Address in one line", help='If it is'
                            'true it will show address in one line on website')
    hide_marker_icons = fields.Boolean("Hide Marker Icons",
                                       help='If it is true it will hide all '
                                            'icons of address on website')
    show_phone_icon = fields.Boolean("Show Phone Icons",
                                     help='If it is true it will show only'
                                          ' phone icons on website')
    country_flag = fields.Boolean("Country Flag",
                                  help='If it is true it will show country flag'
                                       ' on website')
    facebook = fields.Boolean("Facebook", help='If it is true it will show '
                                               'company name on website')
    social_facebook = fields.Char(related='company_id.social_facebook',
                                  readonly=False)
    twitter = fields.Boolean("Twitter", help='If it is true it will'
                                             'show twitter on website')
    social_twitter = fields.Char(related='company_id.social_twitter',
                                 readonly=False, help='Twitter account')
    linked_in = fields.Boolean("LinkedIn", help='If it is true it will'
                                                'show linkdin on website')
    social_linked_in = fields.Char(related='company_id.social_linkedin',
                                   readonly=False, help='Linkedin account')
    instagram = fields.Boolean("Instagram", help='If it is true it will '
                                                 'show instagram on website')
    social_instagram = fields.Char(related='company_id.social_instagram',
                                   readonly=False, help='Instagram account')
    git_hub = fields.Boolean("GitHub", help='If it is true it will '
                                            'show github on website',
                             default=False)
    social_git_hub = fields.Char(related='company_id.social_github',
                                 readonly=False, help='Github Account')
