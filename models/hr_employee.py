# -*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models,api
from datetime import date, datetime

class HrContract(models.Model):
    _inherit="hr.employee"
    
    kids = fields.One2many('hr.kids', 'parent', string='Enfants')
    cnps = fields.Char(string='Numéro CNPS')
