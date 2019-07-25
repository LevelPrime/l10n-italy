# -*- coding: utf-8 -*-
# Copyright 2019 Roberto Fichera - Level Prime srl (<https://www.levelprime.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, _
from odoo.exceptions import UserError

from datetime import date

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def _check_invoice_reference(self):
        for invoice in self:
            try:
                super(AccountInvoice, invoice)._check_invoice_reference()
            except UserError:
                # If we get UserError we could try restrict the check by verifying
                # if the bill is in the same year
                year = fields.Date.from_string(invoice.date_invoice).year
                date_start = date(year, 1, 1)
                date_end = date(year, 12, 31)
                if invoice.search([('type', '=', invoice.type),
                                   ('reference', '=', invoice.reference),
                                   ('company_id', '=', invoice.company_id.id),
                                   ('commercial_partner_id', '=', invoice.commercial_partner_id.id),
                                   ('id', '!=', invoice.id),
                                   ('date_invoice', '>=', fields.Date.to_string(date_start)),
                                   ('date_invoice', '<=', fields.Date.to_string(date_end))]):
                    raise UserError(
                        _("Duplicated vendor reference detected. You probably encoded twice the same"
                          " vendor bill/refund."))