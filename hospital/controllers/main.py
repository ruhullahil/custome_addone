from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleInherit(WebsiteSale):

    @http.route([
        '''/shop''',
        '''/shop/page/<int:page>''',
        '''/shop/category/<model("product.public.category", "[('website_id', 'in', (False, current_website_id))]"):category>''',
        '''/shop/category/<model("product.public.category", "[('website_id', 'in', (False, current_website_id))]"):category>/page/<int:page>'''
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        res = super(WebsiteSaleInherit, self).shop(page=0, category=None, search='', ppg=False, **post)
        print("Inherited Odoo Mates ....", res)
        return res

class Hospital(http.Controller):
    @http.route('/hospital/doctor', website=True, auth='public')
    def hospital_doctor(self, **kwargs):
        doctor = request.env['hospital.doctor'].search([])
        print('doctor : ', len(doctor))

        return request.render('hospital.doctor', {'doctor': doctor})
        # return {'doctor': doctor}

    @http.route('/hospital/get-patents', type='json',methods=['GET'], auth='user')
    def get_patient(self):
        patien = request.env['hospital.patient'].search([])
        patient_list = []
        for doct in patien:
            single_patient = {
                'name': doct.name,
                'date_of_bath': doct.date_of_bath,
                'address': doct.address
            }
            patient_list.append(single_patient)
        print(patient_list)
        return {'status': 200,
                'data': patient_list,
                'message': 'success'
                }

    @http.route('/hospital/create-patents', type='json',methods=['POST'], auth='user')
    def create_patient(self, **rec):
        if request.jsonrequest:
            print("rec", rec)
            if rec['name']:
                # vals = {
                #     'name': rec['name'],
                #     'date_of_bath': rec['birth_day']
                # }
                new_patient = request.env['hospital.patient'].sudo().create(rec)
                print("New Patient Is", new_patient)
                args = {'success': True, 'message': 'Success', 'id': new_patient.id}
        return args

    @http.route('/hospital/update-patents', type='json', auth='user')
    def update_patient(self, **rec):
        if request.jsonrequest:
            arg={}
            if rec['id']:
                print("rec...", rec)
                patient = request.env['hospital.patient'].sudo().search([('id', '=', rec['id'])])
                if patient:
                    patient.sudo().write(rec)
                    args = {'success': True, 'message': 'Patient Updated'}
                else:
                    args = {'success': False, 'message': 'provide correct id'}

        return args
