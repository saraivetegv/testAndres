
{
    'name': 'odoo1',
    'version': '1.0',
    'author': 'Sara Gomez',
    'category': 'Predios',
    'description':"",
    'depends': [
        'base','sale','base_setup', 'product', 'analytic', 'report', 'web_planner',
    ],
    'data': ['views/views_odoo1.xml','views/views_odoo1_ventasclientes.xml']
}