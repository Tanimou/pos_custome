# -*- coding: utf-8 -*-

from . import models
from odoo import api, SUPERUSER_ID

def _delete(env):
    env["hr.payslip.line"].search([]).unlink()
    env["hr.salary.rule"].search([]).unlink()
    env["hr.salary.rule.category"].search([]).unlink()


def _write_payroll_structure(env):
    env['hr.payroll.structure'].search([("name",'=', 'Regular Pay')]).update({'name': "Salaire régulier"})
def _create_regle_categorie(env):
    env["hr.salary.rule.category"].create([
        {"name":"Retenue employé","code":"RE","parent_id":""},
        {"name":"Retenue Patronal","code":"RP","parent_id":""},
        {"name":"Total prime non imposable","code":"TPNI","parent_id":""},
        {"name":"Brut","code":"BT","parent_id":""},
        {"name":"Prime non imposable","code":"PNI","parent_id":""},
        {"name":"Salaire net","code":"SN","parent_id":""},
        {"name":"Salaire brut imposable","code":"SBI","parent_id":env["hr.salary.rule.category"].search([("code","=","SN")]).id},
        {"name":"Prime imposable","code":"PI","parent_id":env["hr.salary.rule.category"].search([("code","=","SBI")]).id},
        {"name":"Retenue fiscale","code":"RF","parent_id":env["hr.salary.rule.category"].search([("code","=","SN")]).id},
        {"name":"Retenue sociale employé","code":"RSE","parent_id":env["hr.salary.rule.category"].search([("code","=","SN")]).id},
        {"name":"Retenue sociale patronale","code":"RSP","parent_id":""},
        {"name":"Retenue fiscale patronale","code":"RFP","parent_id":""},
        {"name":"Autre","code":"AU","parent_id":""}
                                           ])
def _create_rules(env):
    env["hr.salary.rule"].create([
        # 1
        {
            "name":"Salaire catégoriel",
            "category_id":env["hr.salary.rule.category"].search([("code","=","SBI")]).id,
            "code":"BASIC",
            "struct_id":env["hr.payroll.structure"].search([("name","=","Salaire régulier")]).id,
            "sequence":1,"active":True,
            "appears_on_payslip":True,
            "appears_on_payroll_report":False,
            "amount_select":"code",
            "amount_python_compute":"result = contract.salary",
            "condition_select":"none",
    
            },
        # 2
        {
            "name":"Sur salaire",
            "category_id":env["hr.salary.rule.category"].search([("code","=","SBI")]).id,
            "code":"SUS",
            "struct_id":env["hr.payroll.structure"].search([("name","=","Salaire régulier")]).id,
            "sequence":2,
            "active":True,
            "appears_on_payslip":True,
            "appears_on_payroll_report":False,
            "amount_select":"code",
            "amount_python_compute":"result = contract.su_salary",
            "condition_select":"none",
    
            },
        # 3
        {
            "name":"Prime d'ancienneté",
            "category_id":env["hr.salary.rule.category"].search([("name","=","Prime imposable")]).id,
            "code":"PA",
            "struct_id":env["hr.payroll.structure"].search([("name","=","Salaire régulier")]).id,
            "sequence":3,
            "active":True,
            "appears_on_payslip":True,
            "appears_on_payroll_report":False,
            "amount_select":"code",
            "amount_python_compute":"result = contract.seniority_bonus",
            },
        # 4
        {
            "name":"Prime de carburant",
            "category_id":env["hr.salary.rule.category"].search([("name","=","Prime imposable")]).id,
            "code":"PC",
            "struct_id":env["hr.payroll.structure"].search([("name","=","Salaire régulier")]).id,
            "sequence":4,
            "active":True,
            "appears_on_payslip":True,
            "appears_on_payroll_report":False,
            "amount_select":"code",
            "amount_python_compute":"result = contract.prime_carburant",
            "condition_select":"none",
            },
        # 5
        {
            "name":"Assurance",
            "category_id":env["hr.salary.rule.category"].search([("name","=","Prime imposable")]).id,
            "code":"AS",
            "struct_id":env["hr.payroll.structure"].search([("name","=","Salaire régulier")]).id,
            "sequence":5,
            "active":True,
            "appears_on_payslip":True,
            "appears_on_payroll_report":False,
            "amount_select":"code",
            "amount_python_compute":"result = contract.assurance",
            "condition_select":"none",

            },
        # 6
        {
            "name":"Prime de responsabilité",
            "category_id":env["hr.salary.rule.category"].search([("name","=","Prime imposable")]).id,
            "code":"PRE",
            "struct_id":env["hr.payroll.structure"].search([("name","=","Salaire régulier")]).id,
            "sequence":6,
            "active":True,
            "appears_on_payslip":True,
            "appears_on_payroll_report":False,
            "amount_select":"code",
            "amount_python_compute":"result = contract.prime_resp",
            "condition_select":"none",

            },
    # 24
        # 7
        {
            "name":"Prime de transport imposable",
            "category_id":env["hr.salary.rule.category"].search([("name","=","Prime imposable")]).id,
            "code":"PTI",
            "struct_id":env["hr.payroll.structure"].search([("name","=","Salaire régulier")]).id,
            "sequence":7,"active":True,
            "appears_on_payslip":True,
            "appears_on_payroll_report":False,
            "amount_select":"code",
            "amount_python_compute":"result = contract.taxable_transportation_allowance",
    
            },
        # 8
        {
            "name":"Prime de logement",
            "category_id":env["hr.salary.rule.category"].search([("name","=","Prime imposable")]).id,
            "code":"PL",
            "struct_id":env["hr.payroll.structure"].search([("name","=","Salaire régulier")]).id,
            "sequence":8,"active":True,
            "appears_on_payslip":True,
            "appears_on_payroll_report":False,
            "amount_select":"code",
            "amount_python_compute":"result = contract.prime_logement",
            "condition_select":"none",
    
            },
        # 9
        {
            "name":"Heures supplémentaires",
            "category_id":env["hr.salary.rule.category"].search([("name","=","Prime imposable")]).id,
            "code":"HRS",
            "struct_id":env["hr.payroll.structure"].search([("name","=","Salaire régulier")]).id,
            "sequence":9,"active":True,
            "appears_on_payslip":True,
            "appears_on_payroll_report":False,
            "amount_select":"fix",
            "quantity":"1",
            "amount_fix":0,
            "condition_select":"none",
    
        },

        {
            "name": "Salaire brut",
            "category_id": env["hr.salary.rule.category"].search([("name", "=", "Brut")]).id,
            "code": "SB",
            "struct_id": env["hr.payroll.structure"].search([("name", "=", "Salaire régulier")]).id,
            "sequence": 25, "active": True,
            "appears_on_payslip":True,
            "appears_on_payroll_report":False,
            "amount_select":"code",
            "amount_python_compute":"result = categories.SBI + categories.PI",
            "condition_select":"none",
        },
        # 10
        {
            "name":"Retenue sur absence",
            "category_id":env["hr.salary.rule.category"].search([("name","=","Autre")]).id,
            "code":"RA",
            "struct_id":env["hr.payroll.structure"].search([("name","=","Salaire régulier")]).id,
            "sequence":30,"active":True,
            "appears_on_payslip":True,
            "appears_on_payroll_report":False,
            "amount_select":"code",
            "amount_python_compute":"result = payslip.retenu_absence",
            "condition_select":"none",
    
            },
        # 11
        {
            "name":"Impôt sur salaire employé",
            "category_id":env["hr.salary.rule.category"].search([("name","=","Retenue fiscale")]).id,
            "code":"ISE",
            "struct_id":env["hr.payroll.structure"].search([("name","=","Salaire régulier")]).id,
            "sequence":700,"active":True,
            "appears_on_payslip":True,
            "appears_on_payroll_report":False,
            "amount_select":"percentage",
            "amount_percentage_base":"contract.wage",
            "amount_percentage":1.2,
            "quantity":"1",
            "condition_select":"none",
    
            },
        # 12
        {
            "name":"Contribution nationale",
            "category_id":env["hr.salary.rule.category"].search([("name","=","Retenue fiscale")]).id,
            "code":"CN",
            "struct_id":env["hr.payroll.structure"].search([("name","=","Salaire régulier")]).id,
            "sequence":701,"active":True,
            "appears_on_payslip":True,
            "appears_on_payroll_report":False,
            "amount_select":"code",
            "amount_python_compute":"result = payslip.national_contribution",
            "condition_select":"none",
    
            },
        # 13
        {
            "name":"Impôt général sur les revenus",
            "category_id":env["hr.salary.rule.category"].search([("name","=","Retenue fiscale")]).id,
            "code":"IGR",
            "struct_id":env["hr.payroll.structure"].search([("name","=","Salaire régulier")]).id,
            "sequence":702,"active":True,
            "appears_on_payslip":True,
            "appears_on_payroll_report":False,
            "amount_select":"code",
            "amount_python_compute":"result = payslip.general_income_tax",
            "condition_select":"none",
    
            },
        # 14
        {
            "name":"CMU employé",
            "category_id":env["hr.salary.rule.category"].search([("name","=","Retenue sociale employé")]).id,
            "code":"CMUE",
            "struct_id":env["hr.payroll.structure"].search([("name","=","Salaire régulier")]).id,
            "sequence":801,"active":True,
            "appears_on_payslip":True,
            "appears_on_payroll_report":False,
            "amount_select":"code",
            "amount_python_compute":"result = payslip.cmu",
            "condition_select":"none",
    
            },
        # 15
        {
            "name":"CNPS employé",
            "category_id":env["hr.salary.rule.category"].search([("name","=","Retenue sociale employé")]).id,
            "code":"CRE",
            "struct_id":env["hr.payroll.structure"].search([("name","=","Salaire régulier")]).id,
            "sequence":802,"active":True,
            "appears_on_payslip":True,
            "appears_on_payroll_report":False,
            "amount_select":"percentage",
            "amount_percentage_base":"contract.wage",
            "amount_percentage":6.3,
            "quantity":"1",
            "condition_select":"none",
    
            },
        {
            "name": "Total retenue employé",
            "category_id": env["hr.salary.rule.category"].search([("name", "=", "Retenue employé")]).id,
            "code": "TRE",
            "struct_id": env["hr.payroll.structure"].search([("name", "=", "Salaire régulier")]).id,
            "sequence": 901, "active": True,
            "appears_on_payslip": True,
            "appears_on_payroll_report": False,
            "amount_select":"code",
            "amount_python_compute":"result = categories.RSE + categories.RF",
            "condition_select":"none",
        },
        # 16
        {
            "name":"Assurance maternité",
            "category_id":env["hr.salary.rule.category"].search([("name","=","Retenue sociale patronale")]).id,
            "code":"AM",
            "struct_id":env["hr.payroll.structure"].search([("name","=","Salaire régulier")]).id,
            "sequence":902,"active":True,
            "appears_on_payslip":True,
            "appears_on_payroll_report":False,
            "amount_select":"percentage",
            "amount_percentage_base":"75000",
            "amount_percentage":0.75,
            "quantity":"1",
            "condition_select":"none",
    
            },
        # 17
        {
            "name":"Accident de travail",
            "category_id":env["hr.salary.rule.category"].search([("name","=","Retenue sociale patronale")]).id,
            "code":"AT",
            "struct_id":env["hr.payroll.structure"].search([("name","=","Salaire régulier")]).id,
            "sequence":903,"active":True,
            "appears_on_payslip":True,
            "appears_on_payroll_report":False,
            "amount_select":"percentage",
            "amount_percentage_base":"75000",
            "amount_percentage":2.0,
            "quantity":"1",
            "condition_select":"none",
    
            },
        # 18
        {
            "name":"Prestation familiale",
            "category_id":env["hr.salary.rule.category"].search([("name","=","Retenue sociale patronale")]).id,
            "code":"PF",
            "struct_id":env["hr.payroll.structure"].search([("name","=","Salaire régulier")]).id,
            "sequence":905,"active":True,
            "appears_on_payslip":True,
            "appears_on_payroll_report":False,
            "amount_select":"percentage",
            "amount_percentage_base":"75000",
            "amount_percentage":5,
            "quantity":"1",
            "condition_select":"none",
    
            },
        # 19
        {
            "name":"Retraite générale",
            "category_id":env["hr.salary.rule.category"].search([("name","=","Retenue sociale patronale")]).id,
            "code":"CR",
            "struct_id":env["hr.payroll.structure"].search([("name","=","Salaire régulier")]).id,
            "sequence":906,"active":True,
            "appears_on_payslip":True,
            "appears_on_payroll_report":False,
            "amount_select":"percentage",
            "amount_percentage_base":"contract.wage",
            "amount_percentage":7.7,
            "quantity":"1",
            "condition_select":"none",
    
            },
        # 20
        {
            "name":"CMU employeur",
            "category_id":env["hr.salary.rule.category"].search([("name","=","Retenue sociale patronale")]).id,
            "code":"CMU",
            "struct_id":env["hr.payroll.structure"].search([("name","=","Salaire régulier")]).id,
            "sequence":907,"active":True,
            "appears_on_payslip":True,
            "appears_on_payroll_report":False,
            "amount_select":"code",
            "amount_python_compute":"result = payslip.cmu_patronale",
            "condition_select":"none",
    
            },
        # 21
        {
            "name":"Taxe apprentissage",
            "category_id":env["hr.salary.rule.category"].search([("name","=","Retenue fiscale patronale")]).id,
            "code":"TF",
            "struct_id":env["hr.payroll.structure"].search([("name","=","Salaire régulier")]).id,
            "sequence":951,"active":True,
            "appears_on_payslip":True,
            "appears_on_payroll_report":False,
            "amount_select":"percentage",
            "amount_percentage_base":"contract.wage",
            "amount_percentage":0.4,
            "quantity":"1",
            "condition_select":"none",
    
            },
        # 22
        {
            "name":"Impôt sur salaire et traitement patronal",
            "category_id":env["hr.salary.rule.category"].search([("name","=","Retenue fiscale patronale")]).id,
            "code":"ISP",
            "struct_id":env["hr.payroll.structure"].search([("name","=","Salaire régulier")]).id,
            "sequence":952,"active":True,
            "appears_on_payslip":True,
            "appears_on_payroll_report":False,
            "amount_select":"percentage",
            "amount_percentage_base":"contract.wage",
            "amount_percentage":1.2,
            "quantity":"1",
            "condition_select":"none",
    
            },
        # 23
        {
            "name":"Taxe formation professionnelle continue",
            "category_id":env["hr.salary.rule.category"].search([("name","=","Retenue fiscale patronale")]).id,
            "code":"TFPC",
            "struct_id":env["hr.payroll.structure"].search([("name","=","Salaire régulier")]).id,
            "sequence":953,"active":True,
            "appears_on_payslip":True,
            "appears_on_payroll_report":False,
            "amount_select":"percentage",
            "amount_percentage_base":"contract.wage",
            "amount_percentage":0.6,
            "quantity":"1",
            "condition_select":"none",
    
            },

        {
            "name": "Total retenue patronal",
            "category_id": env["hr.salary.rule.category"].search([("name", "=", "Retenue Patronal")]).id,
            "code": "TRP",
            "struct_id": env["hr.payroll.structure"].search([("name", "=", "Salaire régulier")]).id,
            "sequence": 1000, "active": True,
            "appears_on_payslip": True,
            "appears_on_payroll_report": False,
            "amount_select": "code",
            "amount_python_compute": "result = categories.RSP + categories.RFP",
            "condition_select": "none",

        },
    
        # 25
        {
            "name": "Prime de transport",
            "category_id": env["hr.salary.rule.category"].search([("name", "=", "Prime non imposable")]).id,
            "code": "PT",
            "struct_id": env["hr.payroll.structure"].search([("name", "=", "Salaire régulier")]).id,
            "sequence": 1001, "active": True,
            "appears_on_payslip": True,
            "appears_on_payroll_report": False,
            "amount_select": "code",
            "amount_python_compute": "result = contract.travel_allowance",
            "condition_select": "none",

        },

        {
            "name":"Prime exceptionnelle",
            "category_id":env["hr.salary.rule.category"].search([("name","=","Prime non imposable")]).id,
            "code":"PE",
            "struct_id":env["hr.payroll.structure"].search([("name","=","Salaire régulier")]).id,
            "sequence":1002,"active":True,
            "appears_on_payslip":True,
            "appears_on_payroll_report":False,
            "amount_select":"code",
            "amount_python_compute":"result = contract.prime_exp",
            "condition_select":"none",
    
            },
        # 26
        {
            "name":"Prime de rendement",
            "category_id":env["hr.salary.rule.category"].search([("name","=","Prime non imposable")]).id,
            "code":"PR",
            "struct_id":env["hr.payroll.structure"].search([("name","=","Salaire régulier")]).id,
            "sequence":1003,"active":True,
            "appears_on_payslip":True,
            "appears_on_payroll_report":False,
            "amount_select":"code",
            "amount_python_compute":"result = contract.prime_rend",
            "condition_select":"none",
    
            },
        # 27
        {
            "name":"Prime de panier",
            "category_id":env["hr.salary.rule.category"].search([("name","=","Prime non imposable")]).id,
            "code":"PP",
            "struct_id":env["hr.payroll.structure"].search([("name","=","Salaire régulier")]).id,
            "sequence":1004,"active":True,
            "appears_on_payslip":True,
            "appears_on_payroll_report":False,
            "amount_select":"code",
            "amount_python_compute":"result = contract.prime_pan",
            "condition_select":"none",
    
            },
        # 28
        {
            "name":"Avantage en nature",
            "category_id":env["hr.salary.rule.category"].search([("name","=","Prime non imposable")]).id,
            "code":"AN",
            "struct_id":env["hr.payroll.structure"].search([("name","=","Salaire régulier")]).id,
            "sequence":1005,"active":True,
            "appears_on_payslip":True,
            "appears_on_payroll_report":False,
            "amount_select":"code",
            "amount_python_compute":"result = contract.avtg_nat",
            "condition_select":"none",
    
            },
        # 29
        {
            "name":"Autre prime",
            "category_id":env["hr.salary.rule.category"].search([("name","=","Prime non imposable")]).id,
            "code":"AP",
            "struct_id":env["hr.payroll.structure"].search([("name","=","Salaire régulier")]).id,
            "sequence":1006,"active":True,
            "appears_on_payslip":True,
            "appears_on_payroll_report":False,
            "amount_select":"code",
            "amount_python_compute":"result = contract.other_prime",
            "condition_select":"none",
    
            },

        {
            "name": "Total prime non imposable",
            "category_id": env["hr.salary.rule.category"].search([("name", "=", "Total prime non imposable")]).id,
            "code": "TPNI",
            "struct_id": env["hr.payroll.structure"].search([("name", "=", "Salaire régulier")]).id,
            "sequence": 1100, "active": True,
            "appears_on_payslip": True,
            "appears_on_payroll_report": False,
            "amount_select": "code",
            "amount_python_compute": "result = categories.PNI",
            "condition_select": "none",
        },
        # 30
        {
            "name":"Net de paie",
            "category_id":env["hr.salary.rule.category"].search([("name","=","Salaire net")]).id,
            "code":"SNP",
            "struct_id":env["hr.payroll.structure"].search([("name","=","Salaire régulier")]).id,
            "sequence":1101,"active":True,
            "appears_on_payslip":True,
            "appears_on_payroll_report":False,
            "amount_select":"code",
            "amount_python_compute":"result = categories.SBI + categories.PI - categories.RSE - categories.RF",
            "condition_select":"none",
    
            },
        # 31
        {
            "name":"Salaire net à payer",
            "category_id":env["hr.salary.rule.category"].search([("name","=","Salaire net")]).id,
            "code":"NET",
            "struct_id":env["hr.payroll.structure"].search([("name","=","Salaire régulier")]).id,
            "sequence":1102,"active":True,
            "appears_on_payslip":True,
            "appears_on_payroll_report":False,
            "amount_select":"code",
            "amount_python_compute":"result = payslip.arrondir_trois_derniers_chiffres(categories.SBI + categories.PI - categories.RSE - categories.RF + categories.PNI - categories.AU)",
            "condition_select":"none",
    
            },
    ])
def _post_init_hook(cr, registry):
        env = api.Environment(cr, SUPERUSER_ID, {})
        _delete(env)
        _write_payroll_structure(env)
        _create_regle_categorie(env)
        _create_rules(env)
