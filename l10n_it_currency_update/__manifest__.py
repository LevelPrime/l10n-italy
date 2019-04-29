# -*- coding: utf-8 -*-
# Copyright 2019 Giacomo Grasso, Gabriele Baldessari
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Bank of Italy currency update',
    'version': '10.0.1.0.0',
    'category': 'Accounting & Finance',
    'summary': 'Modulo per aggiornare i tassi di cambio automaticamente '
               'con i dati della Banca d\'Italia.',
    'author': 'Giacomo Grasso, Gabriele Baldessari,'
              'Odoo Community Association (OCA)',
    'website': 'http://www.odoo-community.org',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'currency_rate_update'],
    'data': [],
    'installable': True,
    'auto-install': False,
}
