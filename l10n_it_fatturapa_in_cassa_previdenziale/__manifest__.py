# -*- coding: utf-8 -*-
# Copyright 2019 Roberto Fichera <https://wwww.leveprime.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Italian Localization - Fattura elettronica - Integrazione '
            'Cassa Previdenziale',
    'summary': 'Modulo ponte tra ricezione fatture elettroniche e Cassa '
               'Previdenziale.',
    'version': '10.0.1.0.0',
    'development_status': 'Beta',
    'category': 'Hidden',
    'website': 'https://github.com/OCA/l10n-italy',
    'author': 'Roberto Fichera, Odoo Community Association (OCA)',
    'license': 'LGPL-3',
    'depends': [
        'l10n_it_fatturapa_in',
        'l10n_it_fatturapa_out_wt',
    ],
    'data': [],
    'installable': True,
    'auto_install': True,
}
