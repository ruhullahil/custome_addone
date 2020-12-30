from odoo import models, fields, _


class CreateAppointment(models.TransientModel):
    _name = 'create.appointment'

    def action_lost_reason_apply(self):
        appointment_val = {
            'patient_name': self.patient_id.id,
            'appointment_date': self.appointment_date

        }
        self.patient_id.message_post(body='appointment created', subject='appointment')
        new_appointment = self.env['hospital.appintment'].create(appointment_val)
        return {
            'name': _('appointment'),
            "view_mode": 'form',
            'res_model': 'hospital.appintment',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'res_id': new_appointment.id
        }

    def print_patient_report(self):
        data = {
            'model': 'create.appointment',
            'form': self.read()[0]
        }
        print('print : ', self)
        d_id = self.read()[0]['patient_id'][0]
        return self.env.ref('hospital.record_id').with_context(landscape=True).report_action(d_id)

    def get_data(self):
        appointments = self.env['hospital.appintment'].search([])
        for rec in appointments:
            print("Appointment Name", rec.patient_name)
        # How to Prevent Wizard Getting Closed After Button Click
        # https://www.youtube.com/watch?v=n5La3aTue7o&list=PLqRRLx0cl0hoJhjFWkFYowveq2Zn55dhM&index=68
        return {
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'create.appointment',
            'res_id': self.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    patient_id = fields.Many2one('hospital.patient', string='patient id')
    appointment_date = fields.Date(string="Appointment Date")
