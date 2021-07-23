from odoo import http
from odoo.http import request

class HrEmployee(http.Controller):
    @http.route('/hr_employee/create_from_hris', auth='public', type='json', csrf=False)
    def create_employee_from_hris(self, datas):
        created_employee = request.env['hr.employee'].sudo().create(datas)
        return ("Success create employee with ID " + str(created_employee.id))

    http.route('/hr_employee/update_from_hris', auth='public', type='json', csrf=False)
    def update_employee_from_hris(self, datas):
        employee = request.env['hr.employee'].search([('nik_temp', '=', datas.nik_temp)], limit=1)
        employee.write(datas)
        return ("Success edited employee with ID " + str(employee.id))