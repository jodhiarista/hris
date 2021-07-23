from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import ValidationError

import requests

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    nik_temp = fields.Char(string="NIK Temp", help="Field for sync data from HRIS", readonly=True)

    def get_all_employee_hris(self):
        obj_employee = self.env['hr.employee']
        try:
            employees = requests.get('http://172.16.110.118:7001/api/Karyawan/GetKaryawan/56')
            employees = employees.json()
            employee_ids = []
            for employee in employees:
                employee_id = obj_employee.create({
                    'name': employee['NamaKaryawan']
                    })
                employee_ids.append({
                    'NIK': employee['NIK'],
                    'odoo_employee_id': employee_id.id
                })
        except Exception as E:
                self.env.cr.rollback()
                raise ValidationError(_(E))
        print (employee_ids)
        # return call back buat update record employees dengan data dari employee_ids