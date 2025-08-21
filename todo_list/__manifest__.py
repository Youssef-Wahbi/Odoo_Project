{
    "name": "To Do List",
    "version": "17.0.1.0.0",
    "category": "Custom Apps",
    'summary': '',
    'description': '',
    "author": "",
    "depends": [
        "base",
        "mail",
        "sale_management",
        "stock",
        "contacts",
        "account",
        #"account_accountant",
        "crm",
        "purchase",
        "contacts",

    ],
    "data": [
         "security/security.xml",
         "data/sequence.xml",
         "data/employee_data.xml",
         "data/tasks_data.xml",
         "reports/todo_report.xml",
         "views/base_menu.xml",
         "views/todo_views.xml",
         "views/employee_views.xml",
         "views/bulk_assignment_wizard_views.xml",
         "views/workload_chart_views.xml",
        "security/ir.model.access.csv",
         

        # "views/owner_view.xml",
        # "views/tag_view.xml",


    ],

    "assets":{

        'web.assets_backend':['todo_list/static/src/todo.css']
    },

    'images': ['static/description/to.png'],

    "installable": True,
    "application": True,
}
