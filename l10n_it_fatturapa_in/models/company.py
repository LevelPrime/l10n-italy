# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResCompany(models.Model):
    _inherit = 'res.company'
    cassa_previdenziale_product_id = fields.Many2one(
        'product.product', 'Welfare Fund Data Product',
        help="Product used to model DatiCassaPrevidenziale XML element "
             "on bills."
    )
    sconto_maggiorazione_product_id = fields.Many2one(
        'product.product', 'Discount Supplement Product',
        help="Product used to model ScontoMaggiorazione XML element on bills."
        )
    arrotondamenti_attivi_account_id = fields.Many2one(
        'account.account', 'Active Rounding Account',
        domain=[('deprecated', '=', False)],
        help="Account used for active rounding amount on bills."
        )
    arrotondamenti_passivi_account_id = fields.Many2one(
        'account.account', 'Passive Rounding Account',
        domain=[('deprecated', '=', False)],
        help="Account used for passive rounding amount on bills."
        )
    arrotondamenti_tax_id = fields.Many2one(
        'account.tax', 'Rounding Tax',
        domain=[('type_tax_use', '=', 'purchase'), ('amount', '=', 0.0)],
        help="Tax used for rounding amount on bills."
        )


class AccountConfigSettings(models.TransientModel):
    _inherit = 'account.config.settings'
    cassa_previdenziale_product_id = fields.Many2one(
        related='company_id.cassa_previdenziale_product_id',
        string="Welfare Fund Data Product",
        help="Product used to model DatiCassaPrevidenziale XML element "
             "on bills."
    )
    sconto_maggiorazione_product_id = fields.Many2one(
        related='company_id.sconto_maggiorazione_product_id',
        string="Discount Supplement Product",
        help="Product used to model ScontoMaggiorazione XML element on bills."
        )
    arrotondamenti_attivi_account_id = fields.Many2one(
        related='company_id.arrotondamenti_attivi_account_id',
        string='Active Rounding Account',
        domain=[('deprecated', '=', False)],
        help="Account used for active rounding amount on bills.",
        readonly=False,
        )
    arrotondamenti_passivi_account_id = fields.Many2one(
        related='company_id.arrotondamenti_passivi_account_id',
        string='Passive Rounding Account',
        domain=[('deprecated', '=', False)],
        help="Account used for passive rounding amount on bills.",
        readonly=False,
        )
    arrotondamenti_tax_id = fields.Many2one(
        related='company_id.arrotondamenti_tax_id',
        domain=[('type_tax_use', '=', 'purchase'), ('amount', '=', 0.0)],
        string='Rounding Tax',
        help="Tax used for rounding amount on bills.",
        readonly=False,
        )

    @api.onchange('company_id')
    def onchange_company_id(self):
        res = super(AccountConfigSettings, self).onchange_company_id()
        if self.company_id:
            company = self.company_id
            self.cassa_previdenziale_product_id = (
                company.cassa_previdenziale_product_id and
                company.cassa_previdenziale_product_id.id or False
            )
            self.sconto_maggiorazione_product_id = (
                company.sconto_maggiorazione_product_id and
                company.sconto_maggiorazione_product_id.id or False
                )
            self.arrotondamenti_attivi_account_id = (
                    company.arrotondamenti_attivi_account_id and
                    company.arrotondamenti_attivi_account_id.id or False
            )
            self.arrotondamenti_passivi_account_id = (
                    company.arrotondamenti_passivi_account_id and
                    company.arrotondamenti_passivi_account_id.id or False
            )
            self.arrotondamenti_tax_id = (
                    company.arrotondamenti_tax_id and
                    company.arrotondamenti_tax_id.id or False
            )
        else:
            self.cassa_previdenziale_product_id = False
            self.sconto_maggiorazione_product_id = False
            self.arrotondamenti_attivi_account_id = False
            self.arrotondamenti_passivi_account_id = False
            self.arrotondamenti_tax_id = False
        return res
