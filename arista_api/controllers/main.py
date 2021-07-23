from odoo import http
from odoo.http import request


class InvoiceAPI(http.Controller):
    
    # def write_off_ar_ap_contact(self):
    # for contact in records:
    #     try:
    #         for business_type in env['fal.business.type'].sudo().search([('active', '=', True)]):
    #             CVG = env['x_customer_vendor_group_branch_dependant'].with_context(active_test=False)
    #             PARTNER = env['res.partner'].with_context(active_test=False)
    #             group = contact.x_studio_cust_vg
    #             company_id = business_type.company_id
    #             Property = env['ir.property'].with_context(force_company=company_id.id, force_business_type=business_type.id)
            
    #             if group:
    #                 ar_ir_properties = Property.sudo().get_multi('property_business_account_receivable_id', CVG._name, [group.id])
    #                 for ar_ir_property in ar_ir_properties:
    #                 if ar_ir_properties[ar_ir_property]:
    #                     Property.sudo().set_multi('property_account_receivable_id', PARTNER._name, {contact.id: ar_ir_properties[ar_ir_property].id})
    #                 ap_ir_properties = Property.sudo().get_multi('property_business_account_payable_id', CVG._name, [group.id])
    #                 for ap_ir_property in ap_ir_properties:
    #                 if ap_ir_properties[ap_ir_property]:
    #                     Property.sudo().set_multi('property_account_payable_id', PARTNER._name, {contact.id: ap_ir_properties[ap_ir_property].id})
    #                 titipan_ir_properties = Property.sudo().get_multi('property_business_account_titipan_id', CVG._name, [group.id])
    #                 for titipan_ir_property in titipan_ir_properties:
    #                 if titipan_ir_properties[titipan_ir_property]:
    #                     Property.sudo().set_multi('property_account_titipan_id', PARTNER._name, {contact.id: titipan_ir_properties[titipan_ir_property].id})
    #                 accrue_ir_properties = Property.sudo().get_multi('property_business_account_accrue_id', CVG._name, [group.id])
    #                 for accrue_ir_property in accrue_ir_properties:
    #                 if accrue_ir_properties[accrue_ir_property]:
    #                     Property.sudo().set_multi('property_account_accrue_id', PARTNER._name, {contact.id: accrue_ir_properties[accrue_ir_property].id})
    #     except Exception as E
    #         env.cr.rollback()
    #         raise Warning(E)

    @http.route('/api/generate_valuation_journal_per_pc', type='json', auth="none")
    def generate_journal(self, records):
        env = request.env
        for pc in records:
            try:
                # First Check if Issue Already Exist
                if not pc.x_studio_issue_journal:
                    # Call 100-4/5
                    if pc.x_studio_po.partner_id.x_studio_cust_vg:
                        action_1004_5 = env['ir.actions.server'].browse(566)
                        ctx = dict(env.context or {})
                        ctx.update({'active_ids': [pc.x_studio_po.partner_id.id], 'active_model': 'res.partner'})
                        action_1004_5.with_context(ctx).run()
            
                    # Master Data
                    product = env['product.product'].search([('x_studio_adms_id', '=', '99')], limit=1)
                    product_context = product.with_context(force_company=pc.x_studio_business_type.company_id.id, force_business_type=pc.x_studio_business_type.id)
                    categ = product.categ_id
                    categ_context = categ.with_context(force_company=pc.x_studio_business_type.company_id.id, force_business_type=pc.x_studio_business_type.id)
                    partner = pc.x_studio_po.partner_id
                    partner_context = partner.with_context(force_company=pc.x_studio_business_type.company_id.id, force_business_type=pc.x_studio_business_type.id)
                    pc_dms_refnum = pc.x_studio_adms_id
                    
                    # Creating Journal Issue
                    account_move_line = []
                    total_accrue_debit = 0
                    total_accrue_credit = 0
                    for pr_line in pc.x_studio_objprlines:
                        for detail in pr_line.x_studio_purchase_order_receive_line_detail:
                            # Creating No Rangka
                            no_rangka = False
                            if detail.x_studio_lot:
                                no_rangka = env['x_no_rangka'].search([('name', '=', detail.x_studio_lot)], limit=1)
                                if not no_rangka:
                                    no_rangka = env['x_no_rangka'].create({'name': detail.x_studio_lot})
                            # Inventory Line    
                            account_move_line.append((0, 0, {
                                'name': 'Penerimaan ' + (pr_line.x_studio_product_dimension.name or '') + ' dari ' + (pc.x_studio_adms_id_x_studio_po or ''),
                                'product_uom_id': product.uom_id.id,
                                'product_id': product.id,
                                'quantity': 1,
                                'ref': pc.x_studio_pcnum,
                                'partner_id': partner.id,
                                'debit': detail.x_studio_cost if pc.x_studio_reciepttype == '1' else 0,
                                'credit': detail.x_studio_cost if pc.x_studio_reciepttype == '2' else 0,
                                'account_id': categ_context.property_stock_valuation_account_id.id,
                                'product_dimension_id': pr_line.x_studio_product_dimension.id,
                                'no_rangka_id': no_rangka and no_rangka.id or False,
                            }))
                            total_accrue_debit += detail.x_studio_cost if pc.x_studio_reciepttype == '2' else 0
                            total_accrue_credit += detail.x_studio_cost if pc.x_studio_reciepttype == '1' else 0
                    # Accrue Line
                    account_move_line.append((0, 0, {
                        'name': 'Penerimaan atas ' + (pc.x_studio_adms_id or '') + ' dari ' + (pc.x_studio_adms_id_x_studio_po or ''),
                        'product_uom_id': product.uom_id.id,
                        'product_id': product.id,
                        'quantity': 1,
                        'ref': pc.x_studio_pcnum,
                        'partner_id': partner.id,
                        'debit': total_accrue_debit,
                        'credit': total_accrue_credit,
                        'account_id': partner_context.property_account_accrue_id.id,
                    }))
                    # Journal Selection
                    journal = pc.x_studio_business_type.x_studio_purchase_receipt if pc.x_studio_reciepttype == '1' else pc.x_studio_business_type.x_studio_purchase_retur
                    # Check Periode
                    can_create_journal = env['account.move'].check_fiscalyear_lock_date_method(company_id = journal.fal_business_type.company_id, fal_business_type_id=journal.fal_business_type, date=pc.x_studio_recieptdate)
                    if not can_create_journal:
                        raise Warning("Error on Periode")
                    am = env['account.move'].with_context(default_journal_id=journal.id).sudo().create({
                        'journal_id': journal.id,
                        'line_ids': account_move_line,
                        'date': pc.x_studio_recieptdate,
                        'ref': pc.x_studio_pcnum,
                        'type': 'entry',
                        'x_studio_dmsrefnumber': pc_dms_refnum,
                    })
                    am.with_context(combine_account=False).action_post()
                    pc.write({'x_studio_issue_journal': am.id})
            except Exception as E:
                env.cr.rollback()
                return Warning(E)
        return am
