# -*- coding: utf-8 -*-
# Copyright 2019 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    intrastat_custom_id = fields.Many2one(
        comodel_name='account.intrastat.custom',
        string="Customs Section")
