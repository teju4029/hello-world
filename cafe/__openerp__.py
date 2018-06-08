{
    'name': 'Cafe Management',
    'version': '0.1',
    'category': 'cafe',
    'description': """
      Cafe Management is a module to help cafe managers and owners find in-depth information in regards to
      item profitability, based on total cost of ingredients and resources used to prepare the item. This
      module is concerned with the variable cost of item production.
""",
    'author': 'Hesham of OdooTec',
    'depends': ['product','train_table'],
    'data': [
        #'wizard/wiz_demo_view.xml',
        'item_view.xml',
        'demo_orm_view.xml',
        #'advanced_views.xml'

    ],
    
   
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
