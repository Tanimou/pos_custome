# -*- coding:utf-8 -*-

from odoo import api, fields, models, _


class ResCompany(models.Model):
    _inherit = 'res.company'

    number_cnps = fields.Char(string="Numéro CNPS")
    base_cnps = fields.Monetary(string="Base CNPS", default=7500.0)
    family_benefit = fields.Monetary(string="Prestation familiale", default=3750.0)
    work_accident_rate = fields.Float(string="Accident de travail", default=2.0, digits=(12, 2))
    family_benefit_rate = fields.Float(string="Prestation familiale", default=5.0, digits=(12, 2))
    maternity_insurance_rate = fields.Float(string="Assurance maternité", default=0.75, digits=(12, 2))
    general_retirement_rate = fields.Float(string='Retraite générale', default=7.7, digits=(12, 2))
    applicable_taxe_rate = fields.Float(string="Taxe d'apprentissage", default=0.4, digits=(12, 2))
    taxe_fpc_rate = fields.Float(string="Taxe FPC", default=0.6, digits=(12, 2))
    cnps_salariale_rate = fields.Float(string="CNPS salariale", default=6.3, digits=(12, 2))
    wage_salary_tax_rate = fields.Float(string="Impôt sur le traitement de salaire", default=1.2, digits=(12, 2))


