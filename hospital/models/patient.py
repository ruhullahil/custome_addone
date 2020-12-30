from odoo import api, fields, models, _, tools
from datetime import date
from odoo.exceptions import ValidationError


class salesUser(models.Model):
    _inherit = "sale.order"
    name_of_salers = fields.Char("saler name")

class ResPartner(models.Model):
    _inherit = 'res.partner'

    company_type = fields.Selection(selection_add=[('om', 'Odoo Mates'), ('odoodev', 'Odoo Dev')])


class HospitalPatient(models.Model):

    def name_get(self):
        # name get function for the model executes automatically
        res = []
        for rec in self:
            res.append((rec.id, '%s - %s' % (rec.name, rec.p_id)))
        return res
    def _cron_start(self):
        print("corn work")

    @api.constrains('date_of_bath')
    def age_validate(self):

        for single in self:
            birthDate = single.date_of_bath
            today = date.today()
            age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
            if age <= 1:
                raise ValidationError(_("enter correct date of bath"))

    @api.onchange('doctor_id')
    def set_doctor_gender(self):
        for single in self:
            single.doctor_gender = single.doctor_id.gender

    def send_patient_mail(self):
        print('send mail')
        template_id = self.env.ref('hospital.patient_card_email_send').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)



    _name = 'hospital.patient'
    _description = ' ith sis for testing amad model name is hostipat patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string=' Name', required=True)
    date_of_bath = fields.Date(string='Date', required=True, index=False, readonly=False,
                               states={'draft': [('readonly', False)]},
                               default=fields.Date.context_today)
    address = fields.Char(string="Address ")
    email = fields.Char(string="Email")
    image = fields.Binary(string="Image", attachment=True)
    p_id = fields.Char(string='Patient Reference', required=True, copy=False, readonly=False,
                       states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    gender = fields.Selection([('male', 'Male'),
                               ('female', 'Female')], default='male', string="Gender")
    active = fields.Boolean("Active", default=True)
    users_id = fields.Many2one('res.users', string="PRO")
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor")
    doctor_gender = fields.Selection([('male', 'Male'),
                                      ('female', 'Female')], default='male', string=" Doctor Gender")

    def print_from_object(self):
        return self.env.ref('hospital.record_id').report_action(self)

    @api.depends('date_of_bath')
    def compute_age(self):

        for single in self:
            birthDate = single.date_of_bath
            today = date.today()
            age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
            if age >= 18:
                single.age_group = 'adult'

            else:
                single.age_group = 'not_adult'

    @api.depends('name')
    def compute_appointment(self):
        self.appointment_count = self.env['hospital.appintment'].search_count([('patient_name', '=', self.name)])

    age_group = fields.Selection([('adult', 'Adult'), ('not_adult', 'Not Adult')], string="age_group",
                                 compute=compute_age)
    appointment_count = fields.Integer(string="Appointment count", compute=compute_appointment)

    def open_pation_appointment(self):
        return {
            'name': _('Product Margins'),
            'domain': [('patient_name', '=', self.name)],
            "view_mode": 'tree,form',
            'res_model': 'hospital.appintment',
            'type': 'ir.actions.act_window',
            'view_id': False,

        }

    @api.model
    def create(self, vals):
        print("------------ : create called")
        if vals.get('p_id', _('New')) == _('New'):
            vals['p_id'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')
        result = super(HospitalPatient, self).create(vals)
        print(result)
        return result
