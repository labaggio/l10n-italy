
{
    'name': 'ITA - Intrastat',
    'version': '12.0.1.0.0',
    'category': 'Account',
    'author': 'Openforce'
              ', Link IT srl, Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-italy/tree/11.0/',
    'license': 'LGPL-3',
    "depends": [
        'sale_management',
        'product',
        'stock',
        'stock_account',
        'uom'
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/intrastat.xml',
        'views/product.xml',
        'views/account.xml',
        'views/config.xml',
        'data/account.intrastat.transation.nature.csv',
        'data/account.intrastat.transport.csv',
        'data/account.intrastat.custom.csv',
        'data/report.intrastat.code.csv',
    ],
    "demo": [
        'demo/product_demo.xml'
    ],
    "installable": True
}
