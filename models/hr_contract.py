# -*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models,api
from datetime import date, datetime

class HrContract(models.Model):
    _inherit="hr.contract"
    
    employee_type_id = fields.Many2one('employee.category',
                                       string="Catégorie d'employé",
                                       domain="[('parent_id','=',False)]"
                                       )
    wage = fields.Monetary(string='Salaire brut', compute='_compute_wage', store=True, required=False, tracking=True)
    prime_carburant = fields.Monetary(string='Prime de carburant', tracking=True)
    assurance = fields.Monetary(string='Assurance', tracking=True)
    prime_resp = fields.Monetary(string='Prime de responsabilité', tracking=True)
    prime_exp = fields.Monetary(string='Prime exceptionnelle', tracking=True)
    prime_rend = fields.Monetary(string='Prime de rendement', tracking=True)
    prime_pan = fields.Monetary(string='Prime de panier', tracking=True)
    avtg_nat = fields.Monetary(string='Avantage en nature', tracking=True)
    other_prime = fields.Monetary(string='Autre prime', tracking=True)
    sub_employee_type_id = fields.Many2one('employee.category',
                                           string="Sous-catégorie d'employé",
                                           domain="[('parent_id','=',employee_type_id)]")
    # day_to_work = fields.Float(string="Jours à travailler", digits=(12, 1), default=30.0)
    # days_worked = fields.Float(string="Jours travaillés", digits=(12, 1))
    # salary_day = fields.Monetary(string='Salaire brute journalier', compute='_compute_salary_day', store=True,
    #                              readonly=True, copy=False, tracking=True)
    # salary_final = fields.Monetary(string='Salaire brute final', compute='_compute_salary_final', store=True,
    #                                readonly=True, copy=False, tracking=True)
    
    struct_id = fields.Many2one('hr.payroll.structure', string='Structure salariale')
    paid_vacation = fields.Monetary(string='Congé payé', tracking=True)
    indemnite_depart_retraite = fields.Monetary(string='Indemnité de depart à la retraite', tracking=True)
    Licensing_compensation = fields.Monetary(string='Indemnité de licenciement', tracking=True)
    gratification = fields.Monetary(string='Gratification', tracking=True)
    Anciennete_horaire = fields.Monetary(string='Ancienneté horaire', compute='compute_ha')
    pa = fields.Monetary(string='Prime Ancienneté a supprimer', tracking=True)
    taxable_transportation_allowance = fields.Monetary(string='Prime de transport imposable', compute='compute_travel',
                                                       store=True)
    method_of_payment = fields.Selection([
        ('espece', 'Espèces'),
        ('cheque', 'Chèque'),
        ('virement', 'Virement Bancaire'),
        ('mobile', 'Mobile Money'),
    ], string="Mode de paiement", tracking=True)
    contrat_duration = fields.Char(compute='_compute_contrat_duration', string="Durée ancienneté", store=True)
    salary = fields.Monetary(string='Salaire de base', compute='_compute_salary', store=True, readonly=False,
                             tracking=True)
    monthly_salary_recall = fields.Monetary(string='Rappel salaire mensuel', tracking=True)
    prime_logement = fields.Monetary(string='Prime de logement', tracking=True)
    schedule_pay = fields.Selection([
        ('monthly', 'Mensuel'),
        ('daily', 'Journalier'),
    ], string='Paie prévue', index=True, default='monthly',
        help="Defines the frequency of the wage payment.", tracking=True)
    salary = fields.Monetary(string='Salaire de base', compute='_compute_salary', store=True, readonly=False,
                             tracking=True)
    su_salary = fields.Monetary(string='Sur-Salaire', tracking=True)
    work_day_month = fields.Float(default=30.0, tracking=True)
    travel_allowance = fields.Monetary(string="Prime de transport", required=True, tracking=True)
    seniority_bonus = fields.Monetary(string='Prime ancienneté', compute='_compute_seniority')
    is_seniority = fields.Boolean(string="Seniority ?", compute="_compute_seniority")
    indemnite_licencement = fields.Monetary(string='Indemnité de licenciement non imposable', tracking=True)
    is_expire = fields.Boolean(string="A expiré", compute='_compute_is_expire', store=True)
    ecart = fields.Integer(string="Ecart", compute='_compute_is_expire', store=True)
    daily_pay = fields.Monetary(string='Salaire journalier', tracking=True)
    work_day = fields.Float(string='Nbr jr à travailler', default=1.0, tracking=True)
    work_day_month = fields.Float(default=30.0, tracking=True)

    @api.depends('salary', 'su_salary', 'seniority_bonus','prime_resp','prime_carburant','prime_logement','Licensing_compensation','indemnite_depart_retraite','gratification','paid_vacation','Anciennete_horaire','taxable_transportation_allowance')
    def _compute_wage(self):
        for rec in self:
            salary = 0
            # vérifier si l'employé est payé à la journée ou au mois
            if rec.schedule_pay == 'monthly':
                salary = rec.salary + rec.su_salary
                # salary = (total_salary * rec.number_day_work) / rec.day_to_work
                
            elif rec.schedule_pay == 'daily':
                salary = rec.daily_pay * rec.work_day

            bonus_taxable = rec.prime_resp + rec.assurance + rec.prime_carburant + rec.prime_logement + rec.Licensing_compensation + rec.indemnite_depart_retraite + rec.gratification + rec.paid_vacation + rec.Anciennete_horaire + rec.taxable_transportation_allowance + rec.seniority_bonus
            # contract_bonus_taxable = rec.contract_id.paid_vacation + rec.contract_id.indemnite_depart_retraite + rec.contract_id.Licensing_compensation + rec.contract_id.gratification + rec.contract_id.Anciennete_horaire + rec.contract_id.taxable_transportation_allowance + rec.contract_id.seniority_bonus
            # mount_hs = rec.mount_15 + rec.mount_50 + rec.mount_75 + rec.mount_100

            rec.wage = salary + bonus_taxable 
    @api.depends('date_end')
    def _compute_is_expire(self):
        """ Fonction permettant de savoir si le contract expire dans moins de 14 jours"""
        for rec in self:
            is_expire = False
            ecart = 0
            if rec.date_end:
                today = date.today()
                delta = rec.date_end - today
                if delta.days <= 14:
                    is_expire = True
                    ecart = delta.days
            rec.is_expire = is_expire
            rec.ecart = ecart

    @api.depends('employee_type_id', 'sub_employee_type_id')
    def _compute_salary(self):
        """ Fonction retournant le salaire de base selon la catégorie de l'employé """
        for rec in self:
            salary = 0
            if rec.employee_type_id and not rec.sub_employee_type_id:
                salary = rec.employee_type_id.salary
            elif rec.employee_type_id and rec.sub_employee_type_id:
                salary = rec.sub_employee_type_id.salary
            rec.salary = salary


    @api.depends('date_start', 'date_end')
    def _compute_contrat_duration(self):
        """ Fonction retournant la durée d'ancienneté """
        today = date.today()
        for rec in self:
            # traitement de la durée d'ancienneté
            date_diff = today - rec.date_start
            years = date_diff.days // 365
            months = (date_diff.days - years * 365) // 30
            rec.contrat_duration = f"{years} an(s) {months} mois"


    @api.depends('date_start', 'date_end')
    def _compute_seniority(self):
        """ Fonction retournant la prime d'ancienneté du contract. """
        for rec in self:
            is_seniority = False
            start = int(rec.date_start.year)
            today = int(date.today().year)
            begin_seniority_bonus = today - start
            if begin_seniority_bonus >= 2:
                begin_seniority_bonus = (rec.salary * int(begin_seniority_bonus)) / 100
                is_seniority = True
            rec.seniority_bonus = begin_seniority_bonus
            rec.is_seniority = is_seniority

    @api.depends('travel_allowance')
    def compute_travel(self):
        """ Fonction permettant de calculer la prime de transport imposable"""
        for rec in self:
            if rec.travel_allowance > 30000:
                rec.taxable_transportation_allowance = rec.travel_allowance - 30000
                rec.travel_allowance = 30000
            # else:
            #     rec.taxable_transportation_allowance = 0


    @api.depends('pa')
    def compute_ha(self):
        """ Fonction permettant de calculer l'horaire d'ancienneté"""
        for rec in self:
            rec.Anciennete_horaire = rec.pa / 173

    
    @api.depends('employee_type_id', 'sub_employee_type_id')
    def _compute_salary(self):
        """ Fonction retournant le salaire de base selon la catégorie de l'employé """
        for rec in self:
            salary = 0
            if rec.employee_type_id and not rec.sub_employee_type_id:
                salary = rec.employee_type_id.salary
            elif rec.employee_type_id and rec.sub_employee_type_id:
                salary = rec.sub_employee_type_id.salary
            rec.salary = salary
