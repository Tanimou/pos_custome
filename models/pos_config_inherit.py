from odoo import models,fields,api


class PosConfigInherit(models.Model):
    _inherit ='pos.config'
    _description ='Point of sale configuration inherit'

    # complementary_currency = fields.Many2many('res.currency','Currency')
    # create a complementary currency field that is a many2many field of res.currency
    complementary_currency = fields.Many2one('res.currency',string='Currency')
    complementary_currency_position = fields.Selection(related='complementary_currency.position', readonly=True)
    complementary_currency_symbol = fields.Char(related='complementary_currency.symbol',string='symbol')
    taux = fields.Float('taux de change', digits=(16,16))


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