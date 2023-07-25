# -*- coding:utf-8 -*-

from odoo import api, fields, models
from datetime import date
from odoo.exceptions import ValidationError
from dateutil import relativedelta


class HrKids(models.Model):
    _name = 'hr.kids'
    _description = 'Hr Kids'

    name = fields.Char(string="Nom de l'enfant")
    date_of_birth = fields.Date(string="Date de naissance")
    age = fields.Integer(string="âge", compute="_compute_age",
                         inverse="_inverse_compute_age",
                         search="_search_age")
    parent = fields.Many2one('hr.employee')
    supported = fields.Boolean(compute='cmu_supported')

    @api.depends('date_of_birth')  # exécute la fonction selon "date_of_birth" a tout instant
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 0

    @api.depends('age')
    def _inverse_compute_age(self):
        for rec in self:
            today = date.today()
            print('Date =', relativedelta.relativedelta(years=rec.age))
            rec.date_of_birth = today - relativedelta.relativedelta(years=rec.age)

    def _search_age(self, operator, value):
        """
        fonction de recherche pour les champs calculés qui ne sont pas stocké, il retourne toujours un domain
        value = retourne la valeur de la recherche
        """
        date_of_birth = date.today() - relativedelta.relativedelta(years=value)
        start_year = date_of_birth.replace(day=1, month=1)
        end_year = date_of_birth.replace(day=31, month=12)
        return [('date_of_birth', '>=', start_year), ('date_of_birth', '<=', end_year)]

    @api.onchange('date_of_birth')
    def cmu_supported(self):
        print("%%% supported")
        for rec in self:
            if rec.age > 21:
                raise ValidationError("Vous pouvez enregistrer que les enfants de moins de 21")
            else:
                rec.supported = True

