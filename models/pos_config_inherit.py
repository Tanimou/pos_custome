from odoo import models,fields,api
from odoo.http import request


class PosConfigInherit(models.Model):
    _inherit ='pos.config'
    _description ='Point of sale configuration inherit'

    complementary_currency = fields.Many2one('res.currency','Currency')
    complementary_currency_symbol=fields.Char(related="complementary_currency.symbol",string="Symbol")
    is_complementary_currency_active = fields.Boolean('Active', default=True)
    complementary_currency_position = fields.Selection(related='complementary_currency.position', readonly=True)

    # create a complementary currency field that is a many2many field of res.currency

    # complementary_currency = fields.Many2many('res.currency',string='Currency')
    # complementary_currency = fields.Many2many(
    #     comodel_name='res.currency',
    #     relation='pos_config_complementary_currency_rel',
    #     column1='config_id',
    #     column2='currency_id',
    #     string='Complementary Currencies'
    # )

    taux = fields.Float('taux de change', digits=(16,16))

    # complementary_currency_ids=[]
    
    # @api.onchange('complementary_currency')
    # def update_currency_ids(self):
            
    #         for currency in self.complementary_currency:
    #             self.complementary_currency_ids.append({'name': currency.name})
    #         print("complementary_currency_ids",self.complementary_currency_ids)


# @api.constrains('pricelist_id', 'use_pricelist', 'available_pricelist_ids', 'journal_id', 'invoice_journal_id', 'payment_method_ids')
# def _check_currencies(self):
#         for config in self:
#             if config.use_pricelist and config.pricelist_id not in config.available_pricelist_ids:
#                 raise ValidationError(_("The default pricelist must be included in the available pricelists."))

#             # Check if the config's payment methods are compatible with its currency
#             for pm in config.payment_method_ids:
#                 if pm.journal_id and pm.journal_id.currency_id and pm.journal_id.currency_id != config.currency_id:
#                     raise ValidationError(_("All payment methods must be in the same currency as the Sales Journal or the company currency if that is not set."))
# ##comment/uncomment
#         # if any(self.available_pricelist_ids.mapped(lambda pricelist: pricelist.currency_id != self.currency_id)):
#         #     raise ValidationError(_("All available pricelists must be in the same currency as the company or"
#         #                             " as the Sales Journal set on this point of sale if you use"
#         #                             " the Accounting application."))
#         if self.invoice_journal_id.currency_id and self.invoice_journal_id.currency_id != self.currency_id:
#             raise ValidationError(_("The invoice journal must be in the same currency as the Sales Journal or the company currency if that is not set."))

# class PosConfigComplementaryCurrencyRel(models.Model):
#     _name = 'pos.config.complementary.currency.rel'
#     _description = 'POS Config Complementary Currency Relation'

#     config_id = fields.Many2one(
#         comodel_name='pos.config',
#         string='POS Config',
#         required=True,
#         ondelete='cascade'
#     )

#     currency_id = fields.Many2one(
#         comodel_name='res.currency',
#         string='Currency',
#         required=True,
#         ondelete='cascade'
#     )
    @api.model
    def update_complementary_currency_active(self, is_active):
        print("is active",is_active)
        "get the config_id from a given url. For example: http://localhost:8069/pos/ui?config_id=1#cids=1"
        pos_config = request.env['pos.config'].sudo().browse(1)

        pos_config.write({'is_complementary_currency_active': is_active})
        # print("Is_complementary_currency_active",pos_config.is_complementary_currency_active)
        return True
    
    
    #inherit the account.bank.statement.line model
    class AccountBankStatementLine(models.Model):
        _inherit = 'account.bank.statement.line'
        _description = 'Account Bank Statement Line'
    
        is_new_currency_selected= fields.Boolean('New Currency Selected', related='pos_session_id.config_id.is_complementary_currency_active')