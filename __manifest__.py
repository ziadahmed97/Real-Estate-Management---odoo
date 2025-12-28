{
    "name":"app one",
    "author":"Ziad Ahmed",
    "description":"app one",
    'depends':['base',
               'sale',
               'account',
               'mail',
               'contacts',
               'web'
               ],
    'data':['security/security.xml',
            'security/ir.model.access.csv',
            'data/sequence.xml',
            'data/data.xml',
            'views/base_menu.xml',
            'views/property_view.xml',
            'views/owner_view.xml',
            'views/tag_view.xml',
            'views/sale_order_view.xml',
            'views/res_partner_view.xml',
            'views/building_view.xml',
            'views/property_history_view.xml',
            'reports/property_report.xml',
            'wizard/change_state_view.xml'],
    'assets':{
             'web.assets_backend': [
                               'AppOne/static/src/css/property.css',
                               'AppOne/static/src/css/listView.css',
                               'AppOne/static/src/js/listView.js',
                               'AppOne/static/src/xml/listView.xml',
                               'AppOne/static/src/xml/formView.xml',
                               'AppOne/static/src/css/formView.css',
                               'AppOne/static/src/js/formView.js',
             ],
        'web.report_assets_common': ['AppOne/static/src/css/font.css']
    },
    "application": True
}