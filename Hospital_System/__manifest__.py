{
    'name': 'Hospital Management',
    'version': '1.0',
    'summary': 'Manage hospital operations',
    'description': 'A module to manage doctors, nurses, patients, and appointments.',
    'author': 'Youssef Wahbi',
    'website': 'http://www.example.com',
    'category': 'Healthcare',
    'depends': ['base','mail','account_accountant','stock','purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/doctor_views.xml',
        'views/nurse_views.xml',
        'views/patient_views.xml',
        'views/appointment_views.xml',
        'views/room_views.xml',
        'views/treatment_views.xml',
        'views/prescription_views.xml',
        'views/menu_views.xml',
        'views/account_move_line_inherit_amount.xml',
        'data/doctor_data.xml',
        'data/nurse_data.xml',
        'data/patient_data.xml',
        'data/appointment_data.xml'
        ],
            
    'assets': {
        'web.assets_backend': [
            'Hospital_System/static/src/css/hospital_styles.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False
}
