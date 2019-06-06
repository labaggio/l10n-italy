{
    'name': 'Dichiarazione Intrastat',
    'version': '11.0.1.0.0',
    'category': 'Account',
    'author': 'Openforce'
            ', Link IT srl, Odoo Community Association (OCA)',
    'website': 'http://linkgroup.it/',
    'license': 'LGPL-3',
    "depends": [
        'l10n_it_intrastat',
    ],
    "data": [
        'data/sequence.xml',
        'security/ir.model.access.csv',
        'security/rules.xml',
        'wizard/export_file_view.xml',
        'views/config.xml',
        'views/intrastat.xml',
    ],
    "demo": [],
    "installable": True
}
