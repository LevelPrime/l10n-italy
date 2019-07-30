# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models, _
from odoo.exceptions import UserError


class WizardImportFatturapa(models.TransientModel):
    _inherit = "wizard.import.fatturapa"

    def set_welfares_fund(
            self, FatturaBody, credit_account_id, invoice, wt_found):
        # if we have set the previous logic by product then call
        # super to behave exactly as before
        if self.env.user.company_id.cassa_previdenziale_product_id:
            super(WizardImportFatturapa, self).set_welfares_fund(
                FatturaBody, credit_account_id, invoice, wt_found)
            return

        if not self.e_invoice_detail_level == '2':
            return

        welfares = FatturaBody.DatiGenerali. \
            DatiGeneraliDocumento.DatiCassaPrevidenziale

        # same thing we don't have any welfare fund entry
        if not welfares:
            super(WizardImportFatturapa, self).set_welfares_fund(
                FatturaBody, credit_account_id, invoice, wt_found)
            return

        WelfareFundLineModel = self.env['welfare.fund.data.line']
        for welfareLine in welfares:
            # Search the matching withholding tax
            wts = self.env['withholding.tax'].search([
                ('wt_types', '=', 'enasarco')])

            if not wts:
                raise UserError(_(
                    "The bill contains Welfare Fund tax with "
                    "Type %s, "
                    "but such a tax is not found in your system. Please "
                    "set it."
                ) % welfareLine.TipoCassa)

            wt_found = False
            for wt in wts:
                if wt.tax == float(welfareLine.AlCassa):
                    wt_found = wt
                    break

            if not wt_found:
                raise UserError(_(
                    "The bill contains Welfare Fund tax with "
                    "Type %s and Tax %s "
                    "but such a tax is not found in your system. Please "
                    "set it."
                ) % (welfareLine.TipoCassa, float(welfareLine.AlCassa)))

            WalferLineVals = self._prepareWelfareLine(
                invoice.id, welfareLine)
            WelfareFundLineModel.create(WalferLineVals)
            found = False
            for line in invoice.invoice_line_ids:
                # search an invoice line having the same amount of the
                # ImportoContributoCassa
                if line.invoice_line_tax_wt_ids:
                    ids = line.invoice_line_tax_wt_ids.ids
                    ids.append(wt_found.id)
                    line.update({
                        'invoice_line_tax_wt_ids': [(6, 0, ids)],
                    })
                    found = True

            # if the welfare fund is not found then try to add it as
            # normal product but this will wrongly calculate the bill
            if not found:
                line_vals = self._prepare_generic_line_data(welfareLine)
                line_vals.update({
                    'name': _(
                        "Welfare Fund: %s (%s)"
                    ) % (wts.name, welfareLine.TipoCassa),
                    'price_unit': float(welfareLine.ImportoContributoCassa),
                    'invoice_id': invoice.id,
                    'account_id': wts.account_payable_id.id,
                    'invoice_line_tax_wt_ids': [(6, 0, [wts.id])],
                })
                self.env['account.invoice.line'].create(line_vals)

        # Update the wittholding tax
        invoice._onchange_invoice_line_wt_ids()
