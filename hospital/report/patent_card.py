from odoo import models, api


class PatientCardExtend(models.AbstractModel):
    _name = 'report.hospital.patient_card_id'
    _description = 'this is used for model extend patient_card'

    @api.model
    def _get_report_values(self, docids, data=None):
        print('docids __: ', docids)
        report = self.env['hospital.patient'].browse(docids[0])
        print('did : ', docids[0])
        appointment = self.env['hospital.appintment'].search([])
        print('appointment', appointment)
        appointment_list = []
        for appoint in appointment:
            single_appointment = {
                'name': appoint.patient_name,
                'date_of_bath': appoint.date_of_bath,
                'date': appoint.appointment_date
            }
            print(appointment_list)
            appointment_list.append(single_appointment)
        print(appointment_list)
        print(report[0].name)
        return {

            'doc_model': 'hospital.patient',
            'docs': report,
            'data': data,

        }
