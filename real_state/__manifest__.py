{
    "name": "Real State",
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
        "account_accountant",
        "crm",
        "purchase",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        "data/sequence.xml",
        "data/data.xml",
        "views/base_menu.xml",
        "views/property_view.xml",
        "views/owner_view.xml",
        "views/res_partner_view.xml",
        "views/property_history.xml",
        "views/wizard_view.xml",
        "views/property_comparison_view.xml",
        "views/building_view.xml",
        "views/offer_view.xml",
        "views/employee_view.xml",
        "views/renter_view.xml",
        # "views/owner_view.xml",
        # "views/tag_view.xml",
        "reports/property_reports.xml"


    ],
    "assets": {
        "web.assets_backend": [
            "real_state/static/src/property.css",
            "real_state/static/src/font.css",
            "real_state/static/src/property_tree.css",
            "real_state/static/src/components/Listview/listview.css",
            "real_state/static/src/components/Listview/listview.js",
            "real_state/static/src/components/Listview/listview.xml"
        ]
    },
    "installable": True,
    "application": True,
}
