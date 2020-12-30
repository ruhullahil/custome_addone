from odoo import api, fields, models, _, tools
from datetime import date
import pytz
from odoo.exceptions import ValidationError


class PationtAppointment(models.Model):
    @api.depends('date_of_bath')
    def computer_age(self):
        for single in self:
            birthDate = single.date_of_bath
            today = date.today()
            single.age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))

    @api.model
    def create(self, vals):
        print("------------ : create called")
        if vals.get('seial', _('New')) == _('New'):
            vals['seial'] = self.env['ir.sequence'].next_by_code('hospital.patient.appointment') or _('New')
        result = super(PationtAppointment, self).create(vals)
        print(result)
        return result

    def action_confirm(self):
        for work in self:
            work.status_bar = 'confirm'

    def action_done(self):
        for work in self:
            work.status_bar = 'complite'

    def appointment_pescribe_delete_o2o(self):
        for rec in self:
            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
            time_in_timezone = pytz.utc.localize(rec.appointment_time).astimezone(user_tz)
            print("Time in UTC -->", rec.appointment_time)
            print("Time in Users Timezone -->", time_in_timezone)
            rec.unlink()
            # rec.appointment_line = [(5, 0, 0)]
            return {
                'name': _('Product Margins'),
                'domain': [],
                "view_mode": 'tree,form',
                'res_model': 'hospital.appintment',
                'type': 'ir.actions.act_window',
                'view_id': False,
            }

    @api.model
    def default_get(self, fields_list):
        res = super(PationtAppointment, self).default_get(fields_list)
        res['patient_name'] = 1
        return res

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for rec in self:
            return {'domain': {'order_id': [('partner_id', '=', rec.partner_id.id)]}}

    _name = 'hospital.appintment'
    _description = 'this is appoint ment module for a user '
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "id desc"

    patient_name = fields.Many2one('hospital.patient', required=True, track_visibility='onchange')
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor')

    date_of_bath = fields.Date(string='Date', required=True, index=False, readonly=False,
                               related='patient_name.date_of_bath')
    appointment_date = fields.Date(string='Date of appointment', required=True, index=False, readonly=False,
                                   track_visibility='onchange')
    partner_id = fields.Many2one('res.partner', string="Customer")
    order_id = fields.Many2one('sale.order', string="Sale Order")

    note = fields.Text(string="note", default="this come from default")
    appointment_line = fields.One2many('hospital.appointment.lines', 'appointment_id', string='Appointment Lines')
    seial = fields.Char(string='Patient Reference', required=True, copy=False, readonly=False,
                        states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    status_bar = fields.Selection([('draft', 'Draft'),
                                   ('confirm', 'Confirm'),
                                   ('complite', 'Complite'),
                                   ('cancel', 'Cancel')], default='draft', string="Status")
    refarence = fields.Char(string="Enter ref")
    ap_note = fields.Char("ap_note")

    age = fields.Integer(string="age", compute=computer_age, store=True)
    appointment_time = fields.Datetime("appointment time")

    # doctor =


class HospitalAppointmentLines(models.Model):
    _name = 'hospital.appointment.lines'
    _description = 'Appointment Lines'

    product_id = fields.Many2one('product.product', string='Medicine')
    product_qty = fields.Integer(string="Quantity")
    appointment_id = fields.Many2one('hospital.appintment', string='Appointment ID')
