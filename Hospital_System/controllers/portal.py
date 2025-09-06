from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal

class PatientPortal(CustomerPortal):

    # Override portal home
    @http.route(['/my'], type='http', auth="user", website=True)
    def home(self, **kw):
        # If logged-in user is a doctor
        doctor = request.env['hospital.doctor'].sudo().search([('user_id', '=', request.env.user.id)], limit=1)
        if doctor:
            return request.redirect('/my/doctor')

        # If logged-in user is a patient
        patient = request.env['hospital.patient'].sudo().search([('user_id', '=', request.env.user.id)], limit=1)
        if patient:
            return request.redirect('/my/patient')

        # Default Odoo portal
        return super().home(**kw)

    # Your patient page
    @http.route('/my/patient', type='http', auth='user', website=True)
    def portal_my_patient(self, **kw):
        patient = request.env['hospital.patient'].sudo().search(
            [('user_id', '=', request.env.user.id)], limit=1
        )
        return request.render('Hospital_System.portal_my_patient', {
            'patient': patient
        })

    @http.route('/my/doctor', type='http', auth='user', website=True)
    def portal_my_doctor(self, **kw):
        doctor = request.env['hospital.doctor'].sudo().search(
            [('user_id', '=', request.env.user.id)], limit=1
        )
        return request.render('Hospital_System.portal_my_doctor', {
            'doctor': doctor,
            'patients': doctor.patient_ids,
        })
