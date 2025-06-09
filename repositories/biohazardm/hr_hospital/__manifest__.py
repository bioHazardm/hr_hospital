{
    'name': 'Hospital Management',
    'version': '1.0',
    'summary': 'Module for hospital management',
    'description': """
        This module helps in managing hospital operations:
        - Doctors management
        - Patients management
        - Diseases tracking
        - Patient visits
    """,
    'category': 'Human Resources',
    'author': 'Biohazard',
    'website': 'https://www.example.com',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/doctor_views.xml',
        'views/patient_views.xml',
        'views/disease_views.xml',
        'views/visit_views.xml',
        'views/menu_views.xml',
        'data/disease_data.xml',
    ],
    'demo': [
        'demo/doctor_demo.xml',
        'demo/patient_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
