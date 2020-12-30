# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'hospital',
    'version' : '1.0',
    'summary': 'hospitqal apps',
    'sequence': 10,
    'description': """test --- """,
    'category': 'others',
    'website': 'https://www.odoo.com/',
    'depends': ['mail','sale','website','board'],
    'data': ['security/security.xml',
             'security/ir.model.access.csv',
             'data/sequence.xml',
             'data/mail_template.xml',
             'data/corn.xml',
             'data/data.xml',
             'views/dashboard.xml',
             'views/apointment_action.xml',
             'views/appointment.xml',
             'views/sale_order.xml',
             'views/template.xml',
             'wizards/create_appointment.xml',
             'data/patient_seq.xml',
             'report/report.xml',
             'report/patient_card.xml',
             'views/settings.xml',
             'views/patient.xml',
             'views/doctor.xml',
             'views/menu.xml',






             ],


    'installable': True,
    'application': True,
    'auto_install': False,

}

