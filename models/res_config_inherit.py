from odoo import models, fields, api

class ResConfigInherit(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_complementary_currency = fields.Many2one(related= 'pos_config_id.complementary_currency',readonly = False)
    pos_taux = fields.Float(related='pos_config_id.taux', readonly=False,digits=(16,16))

    # @api.onchange('pos_complementary_currency')
    # def onchange_complementary_currency(self):
    #     if self.pos_complementary_currency:
    #         self.pos_taux = self.pos_complementary_currency.rate
    #     else:
    #         self.pos_taux = 0.0
     

    
