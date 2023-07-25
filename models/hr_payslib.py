# -*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import babel
from datetime import date, datetime, time
from odoo import fields, models, api, tools

class HrPayslib(models.Model):
    _inherit= 'hr.payslip'
    _description = 'Payslib'

    date = fields.Date('Date Account', default=datetime.today(), states={'draft': [('readonly', False)], 'verify': [('readonly', False)]},
                       readonly=True,
                       help="Keep empty to use the period of the validation(Payslip) date.")
    number = fields.Char(string='Reference', readonly=True, copy=False, help="References",
                         states={'draft': [('readonly', False)]})
    name = fields.Char(string='Payslip Name', readonly=True,
                       states={'draft': [('readonly', False)]})
    number_day_work = fields.Float(string="Nbr de jours travaillés", tracking=True, compute="_compute_day_to_work",
                                   readonly=False, store=True)
    number_day_no_work = fields.Float(string="Absence", compute='_compute_number_day_no_work', readonly=False,
                                      store=True, tracking=True)
    salary_advance = fields.Monetary(string='Avance sur salaire', tracking=True)
    acompte = fields.Monetary(string='Acompte sur salaire', tracking=True)
    wage = fields.Monetary(string='Salaire brut', store=True, compute='_compute_wage')
    HS_15 = fields.Float(string='Heures sup à 15%', tracking=True)
    HS_50 = fields.Float(string='Heures sup à 50%', tracking=True)
    HS_75 = fields.Float(string='Heures sup à 75%', tracking=True)
    HS_100 = fields.Float(string='Heures sup à 100%', tracking=True)
    mount_15 = fields.Monetary(string='Montant HS 15%', store=True, compute='_compute_hourly_rates')
    mount_50 = fields.Monetary(string='Montant HS 50%', store=True, compute='_compute_hourly_rates')
    mount_75 = fields.Monetary(string='Montant HS 75%', store=True, compute='_compute_hourly_rates')
    mount_100 = fields.Monetary(string='Montant HS 100%', store=True, compute='_compute_hourly_rates')
    work_dress_bonus = fields.Monetary(string='Prime de tenue de travail', tracking=True)
    technical_bonus = fields.Monetary(string='Prime de technicité', tracking=True)
    responsibility_bonus = fields.Monetary(string='Prime de responsabilité', tracking=True)
    prime_salissure_imposable = fields.Monetary(string='Prime de salissure', tracking=True)
    basket_bonus = fields.Monetary(string='Prime de Panier', tracking=True)
    travel_allowance = fields.Monetary(string="Prime de transport", compute='_compute_travel_allowance', tracking=True,
                                       readonly=False, store=True)
    exceptional_bonus = fields.Monetary(string='Prime exceptionnelle', tracking=True)
    performance_bonus = fields.Monetary(string='Prime de rendement', tracking=True)
    advantage_in_kind = fields.Monetary(string='Avantage en nature', tracking=True)
    other_bonus = fields.Monetary(string='Autre prime', tracking=True)
    retenu_absence = fields.Monetary(string='Retenu sur absence', tracking=True)
    wage_salary_tax = fields.Monetary(string='Impôt sur traitement de salaire', store=True,
                                      compute='_compute_wage_salary_tax')
    national_contribution = fields.Monetary(string='Contribution nationale', store=True,
                                            compute='_compute_national_contribution')
    net_taxable_income = fields.Monetary(string='Base IGR', store=True,
                                         compute='_compute_net_taxable_income')
    number_of_shares = fields.Float(string='Nombre de part', store=True, compute='_compute_shares')
    income_on_number_of_shares = fields.Monetary(string='Revenu/Nbr de part', store=True, compute='_compute_shares')
    cnps_salariale = fields.Monetary(string='CNPS', store=True, compute='_compute_cnps_salariale')
    general_income_tax = fields.Monetary(string='Impôt général sur revenu', store=True,
                                         compute='_compute_general_income_tax')
    cmu = fields.Monetary(string="CMU employé", compute='_compute_cmu')
    applicable_taxe = fields.Monetary(string="Taxe d'apprentissage", store=True, compute='_compute_applicable_taxe')
    taxe_fpc = fields.Monetary(string='Taxe FPC', store=True, compute='_compute_taxe_fpc')
    general_retirement = fields.Monetary(string='Retraite générale', store=True, compute='_compute_general_retirement')
    work_related_accident = fields.Monetary(string='Accident de travail', store=True,
                                            compute='_compute_work_related_accident')
    family_benefit = fields.Monetary(string='Prestation familiale', readonly=True, related='company_id.family_benefit')
    maternity_insurance = fields.Monetary(string='Assurance maternité', store=True,
                                          compute='_compute_maternity_insurance')
    cmu_patronale = fields.Monetary(string="CMU patronale", compute='_compute_cmu')
    day_to_work = fields.Float(string="Nbr de jours à travaillés", compute="_compute_day_to_work")


    def _get_month(self):
        """ Fonction retournant le mois en cours """
        for line in self:
            ttyme = datetime.combine(fields.Date.from_string(line.date_from), time.min)
            locale = self.env.context.get('lang') or 'en_US'
            return tools.ustr(babel.dates.format_date(date=ttyme, format='MMMM-y', locale=locale))


    @api.depends('contract_id', 'number_day_work')
    def _compute_travel_allowance(self):
        """ Fonction retournant la prime de transport """
        for rec in self:
            travel_allowance = 0
            if rec.contract_id and rec.day_to_work == rec.number_day_work:
                travel_allowance = rec.contract_id.travel_allowance
            elif rec.contract_id and rec.day_to_work != rec.number_day_work:
                travel_allowance = (rec.contract_id.travel_allowance * rec.number_day_work) / rec.day_to_work
            rec.travel_allowance = travel_allowance

    @api.depends('contract_id', 'HS_15', 'HS_50', 'HS_75', 'HS_100')
    def _compute_hourly_rates(self):
        """ Fonction permettant de calculer le montant des heures supplémentaire"""
        for rec in self:
            hourly_rates = 0
            if rec.contract_id.schedule_pay == 'monthly':
                salary = rec.contract_id.salary + rec.contract_id.su_salary
                hourly_rates = salary / 173.33
            elif rec.contract_id.schedule_pay == 'daily':
                hourly_rates = rec.contract_id.daily_pay / 8

            mount_15 = (hourly_rates * 0.15 * rec.HS_15) + hourly_rates
            mount_50 = (hourly_rates * 0.50 * rec.HS_50) + hourly_rates
            mount_75 = (hourly_rates * 0.75 * rec.HS_75) + hourly_rates
            mount_100 = (hourly_rates * rec.HS_100) + hourly_rates

            rec.mount_15 = mount_15 if rec.HS_15 != 0 else 0
            rec.mount_50 = mount_50 if rec.HS_50 != 0 else 0
            rec.mount_75 = mount_75 if rec.HS_75 != 0 else 0
            rec.mount_100 = mount_100 if rec.HS_100 != 0 else 0


    @api.depends('number_day_work')
    def _compute_number_day_no_work(self):
        """ Fonction mettant à jour le nombre de jours d'absence"""
        for rec in self:
            rec.number_day_no_work = rec.day_to_work - rec.number_day_work

    @api.depends('contract_id')
    def _compute_day_to_work(self):
        """ Fonction retournant le nombre de jour à travailler selon le type de contract"""
        for rec in self:
            day_to_work = 0
            if rec.contract_id.schedule_pay == 'monthly':
                day_to_work = rec.contract_id.work_day_month
            elif rec.contract_id.schedule_pay == 'daily':
                day_to_work = rec.contract_id.work_day
            rec.day_to_work = day_to_work
            rec.number_day_work = day_to_work

    @api.depends('company_id')
    def _compute_maternity_insurance(self):
        """ Fonction retournant le montant de l'assurance maternité. """
        for rec in self:
            maternity_insurance = 0
            if rec.company_id:
                maternity_insurance = (rec.company_id.maternity_insurance_rate * rec.company_id.base_cnps) / 100
            rec.maternity_insurance = maternity_insurance

    @api.depends('company_id')
    def _compute_work_related_accident(self):
        """ Fonction retournant le montant de l'accident de travaille. """
        for rec in self:
            work_related_accident = 0
            if rec.company_id:
                work_related_accident = (rec.company_id.work_accident_rate * rec.company_id.base_cnps) / 100
            rec.work_related_accident = work_related_accident

    @api.depends('wage', 'company_id')
    def _compute_general_retirement(self):
        """ Fonction retournant le coût de la retraire générale """
        for rec in self:
            general_retirement = 0
            if rec.company_id:
                general_retirement = (rec.wage * rec.company_id.general_retirement_rate) / 100
            rec.general_retirement = general_retirement

    @api.depends('wage', 'company_id')
    def _compute_taxe_fpc(self):
        """ Fonction retournant le coût de la taxe FPC """
        for rec in self:
            taxe_fpc = 0
            if rec.company_id:
                taxe_fpc = (rec.wage * rec.company_id.taxe_fpc_rate) / 100
            rec.taxe_fpc = taxe_fpc

    @api.depends('wage', 'company_id')
    def _compute_wage_salary_tax(self):
        """ Fonction retournant le montant de l'impôt sur le traitement de salaire"""
        for rec in self:
            wage_salary_tax = 0
            if rec.company_id:
                wage_salary_tax = (rec.wage * 1.2) / 100
            rec.wage_salary_tax = wage_salary_tax
    @api.depends('wage')
    def _compute_national_contribution(self):
        """ Fonction calculant le montant de la contribution nationale"""
        for rec in self:
            national_contribution = rec.wage * 0.8
            if 0 <= national_contribution < 50000:
                rec.national_contribution = 0
            elif 50000 <= national_contribution < 130000:
                rec.national_contribution = (national_contribution * 0.015) - 750
            elif 130000 <= national_contribution < 200000:
                rec.national_contribution = (national_contribution * 0.05) - 5300
            elif national_contribution >= 200000:
                rec.national_contribution = (national_contribution * 0.1) - 15300

    @api.depends('wage_salary_tax', 'national_contribution', 'wage')
    def _compute_net_taxable_income(self):
        """ Fonction calculant la base de l'IGR"""
        for rec in self:
            rec.net_taxable_income = ((rec.wage * 0.8) - (rec.wage_salary_tax + rec.national_contribution)) * 0.85

    @api.depends('net_taxable_income')
    def _compute_shares(self):
        print("heyheyheyheyheyheyheyhey")
        """ Fonction calculant le nombre de parts et le revenu/nombre de parts"""
        for rec in self:
            n = 0
            if rec.employee_id.marital == 'married':
                n += 2
                n += int(rec.employee_id.children) * 0.5
            if rec.employee_id.marital in ['single', 'divorced']:
                if int(rec.employee_id.children) > 0:
                    n += 1.5
                    n += 0.5 * int(rec.employee_id.children)
                else:
                    n = 1
            if rec.employee_id.marital == 'widower':
                if int(rec.employee_id.children) > 0:
                    n += 2
                    n += 0.5 * int(rec.employee_id.children)
                else:
                    n = 1
            if n != 0:
                rec.income_on_number_of_shares = rec.net_taxable_income / n
                rec.number_of_shares = n

    @api.depends('contract_id', 'responsibility_bonus', 'work_dress_bonus', 'technical_bonus', 'prime_salissure_imposable', 'mount_15',
                 'mount_50', 'mount_75', 'mount_100', 'number_day_work')
    def _compute_wage(self):
        """ Fonction calculant le salaire brut """
        for rec in self:
            salary = 0
            # vérifier si l'employé est payé à la journée ou au mois
            if rec.contract_id.schedule_pay == 'monthly':
                total_salary = rec.contract_id.salary + rec.contract_id.su_salary
                salary = (total_salary * rec.number_day_work) / rec.day_to_work
            elif rec.contract_id.schedule_pay == 'daily':
                salary = rec.contract_id.daily_pay * rec.contract_id.work_day

            bonus_taxable = rec.responsibility_bonus + rec.prime_salissure_imposable + rec.work_dress_bonus + rec.technical_bonus
            contract_bonus_taxable = rec.contract_id.paid_vacation + rec.contract_id.indemnite_depart_retraite + rec.contract_id.Licensing_compensation + rec.contract_id.gratification + rec.contract_id.Anciennete_horaire + rec.contract_id.taxable_transportation_allowance + rec.contract_id.seniority_bonus
            mount_hs = rec.mount_15 + rec.mount_50 + rec.mount_75 + rec.mount_100

            rec.wage = salary + bonus_taxable + contract_bonus_taxable + mount_hs


    @api.depends('wage', 'company_id')
    def _compute_cnps_salariale(self):
        """ Fonction retournant le coût de la CNPS salariale """
        for rec in self:
            cnps_salariale = 0
            if rec.company_id:
                cnps_salariale = (rec.wage * rec.company_id.cnps_salariale_rate) / 100
            rec.cnps_salariale = cnps_salariale

    @api.depends('income_on_number_of_shares', 'number_of_shares')
    def _compute_general_income_tax(self):
        data = [
            {'c': 1, 'min': 0, 'max': 25000},
            {'c': 2, 'min': 25000, 'max': 45583},
            {'c': 3, 'min': 45583, 'max': 81583},
            {'c': 4, 'min': 81583, 'max': 126583},
            {'c': 5, 'min': 126583, 'max': 220333},
            {'c': 6, 'min': 220333, 'max': 389083},
            {'c': 7, 'min': 389083, 'max': 842166},
            {'c': 8, 'min': 842167, 'max': 1}
        ]
        for rec in self:
            c = 0
            income_on_number_of_shares = rec.income_on_number_of_shares
            general_income_tax = 0
            for da in data:
                if float(da['min']) <= income_on_number_of_shares <= float(da['max']):
                    c = da['c']
                if float(da['min']) <= income_on_number_of_shares and float(da['max']) == 1:
                    c = da['c']
            if c == 1:
                general_income_tax = 0
            if c == 2:
                general_income_tax = (rec.net_taxable_income * (10 / 110)) - 2273 * rec.number_of_shares
            if c == 3:
                general_income_tax = (rec.net_taxable_income * (15 / 115)) - 4076 * rec.number_of_shares
            if c == 4:
                general_income_tax = (rec.net_taxable_income * (20 / 120)) - 7031 * rec.number_of_shares
            if c == 5:
                general_income_tax = (rec.net_taxable_income * (25 / 125)) - 11250 * rec.number_of_shares
            if c == 6:
                general_income_tax = (rec.net_taxable_income * (35 / 135)) - 24306 * rec.number_of_shares
            if c == 7:
                general_income_tax = (rec.net_taxable_income * (45 / 145)) - 44181 * rec.number_of_shares
            if c == 8:
                general_income_tax = (rec.net_taxable_income * (60 / 160)) - 98633 * rec.number_of_shares
            rec.general_income_tax = general_income_tax
            print("GENERAL INCOME TAX",general_income_tax)

    @api.depends('employee_id')
    def _compute_cmu(self):
        """ Fonction retournant la valeur de la CMU employé et patronale"""
        cmu_employee = 0
        cmu_patronale = 0
        for rec in self:
            if rec.employee_id:
                cmu_employee = 1000
                cmu_patronale = 1000
                kids = self.env['hr.kids'].search([('parent', '=', rec.employee_id.id)])
                if len(kids) <= 6:
                    cmu_employee = ((1000 * len(kids)) + 1000)/2
                    cmu_patronale = ((1000 * len(kids)) + 1000) - cmu_employee
                # if len(kids) > 6:
                #     cmu_extra = len(kids) - 6
                #     cmu_patronale = 3500
                #     cmu_employee = 3500 + (cmu_extra * 1000)
            rec.cmu = cmu_employee
            rec.cmu_patronale = cmu_patronale

    @api.depends('wage', 'company_id')
    def _compute_applicable_taxe(self):
        """ Fonction retournant le coût de la taxe d'apprentissage """
        for rec in self:
            applicable_taxe = 0
            if rec.company_id:
                applicable_taxe = (rec.wage * rec.company_id.applicable_taxe_rate) / 100
            rec.applicable_taxe = applicable_taxe

    def arrondir_trois_derniers_chiffres(nombre):
        dernier_trois_chiffres = nombre % 1000
        if dernier_trois_chiffres < 500:
            return nombre - dernier_trois_chiffres
        elif dernier_trois_chiffres < 750:
            return nombre - dernier_trois_chiffres + 500
        else:
            return nombre - dernier_trois_chiffres + 1000


class ResCompay(models.Model):
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
