# -*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models,api

class HrPayslib(models.Model):
    _inherit= 'hr.salary.rule'
    _description = 'Payslib'
    
    part_salary = fields.Selection([('its', 'ITS'), ('cn', 'CN'), ('igr', 'IGR')], 'Retenue fiscale')
    is_salary = fields.Boolean(string='A partir du salaire')

