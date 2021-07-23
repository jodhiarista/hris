from odoo import fields, models, api, _
from odoo.exceptions import AccessError


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def _get_business_type_default(self):
        user_id = self.env['res.users'].browse(self.env.uid)
        return user_id.fal_business_type_id or False

    fal_business_type = fields.Many2one(
        'fal.business.type', 'Business Type',
        default=_get_business_type_default, index=True,
        help='Let this field empty if this location is shared between business types', domain="[('company_id', '=', company_id)]")

class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'

    def _get_business_type_default(self):
        user_id = self.env['res.users'].browse(self.env.uid)
        return user_id.fal_business_type_id or False

    fal_business_type = fields.Many2one(
        'fal.business.type', 'Business Type',
        default=_get_business_type_default, index=True,
        help='Let this field empty if this location is shared between business types', domain="[('company_id', '=', company_id)]")


class HrPayslipLine(models.Model):
    _inherit = 'hr.payslip.line'

    fal_business_type = fields.Many2one("fal.business.type", string="Business Type", related="slip_id.fal_business_type", store=True)
