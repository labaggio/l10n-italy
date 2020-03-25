#  Copyright 2019 Sergio Corato
#  Copyright 2020 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "ITA - Fattura elettronica - Integrazione SO",
    "summary": "Modulo ponte tra emissione fatture elettroniche e dati "
               "ordine di vendita",
    "version": "12.0.1.0.0",
    "development_status": "Beta",
    "category": "Hidden",
    "website": "https://github.com/OCA/l10n-italy/"
               "12.0/l10n_it_fatturapa_out_sale",
    "author": "Efatto.it, "
              "Agile Business Group, "
              "Odoo Community Association (OCA)",
    "maintainers": ["sergiocorato"],
    "license": "AGPL-3",
    "auto_install": True,
    "depends": [
        "l10n_it_fatturapa_out",
        "sale",
    ],
    "data": [
        "views/partner_view.xml",
        "views/account_view.xml",
    ],
}
