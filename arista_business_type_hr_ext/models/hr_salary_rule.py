from odoo import fields, models, api, _
from odoo.exceptions import AccessError

class HrPayrollStructure(models.Model):
    _inherit = 'hr.payroll.structure'
       
    def _get_business_type_default(self):
        user_id = self.env['res.users'].browse(self.env.uid)
        return user_id.fal_business_type_id or False

    fal_business_type = fields.Many2one(
        'fal.business.type', 'Business Type',
        default=_get_business_type_default, index=True,
        help='Let this field empty if this location is shared between business types')

    journal_id = fields.Many2one('account.journal', 'Salary Journal', readonly=False, required=False,
        company_dependent=True,
        default=lambda self: self.env['account.journal'].sudo().search([
            ('type', '=', 'general'), 
            ('company_id', '=', self.env.company.id), 
            ('fal_business_type', '=', self.env['res.users'].browse(self.env.uid).fal_business_type_id.id)], limit=1))

    