from odoo import http
from odoo.http import request, Response
import io
import xlsxwriter

class DoctorExcelReportController(http.Controller):
    @http.route('/hospital/doctor/excel', type='http', auth='user')
    def doctor_excel_report(self, **kwargs):
        doctors = request.env['hospital.doctor'].sudo().search([])
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Doctors')
        headers = ['Name', 'Specialty', 'Phone', 'Email', 'Hire Date', 'Nurse', 'Salary', 'Active']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header)
        for row, doctor in enumerate(doctors, 1):
            worksheet.write(row, 0, doctor.name)
            worksheet.write(row, 1, doctor.specialty or '')
            worksheet.write(row, 2, doctor.phone or '')
            worksheet.write(row, 3, doctor.email or '')
            worksheet.write(row, 4, str(doctor.hire_date or ''))
            worksheet.write(row, 5, doctor.nurse_id.name or '')
            worksheet.write(row, 6, doctor.salary or 0.0)
            worksheet.write(row, 7, 'Active' if doctor.active else 'Inactive')
        workbook.close()
        output.seek(0)
        xlsx_data = output.read()
        output.close()
        return Response(
            xlsx_data,
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', 'attachment; filename=Doctors.xlsx')
            ],
            status=200
        )
