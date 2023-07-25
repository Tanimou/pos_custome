# -*- coding: utf-8 -*-
{
    'name': "migration de la paye",
    'summary': """,
    custom pos""",
    'description': """
        migration devise
    """,

    'author': "progistack",
    'website': "https://www.progistack.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr_contract','hr_payroll','hr'],

    # always loaded
    'data': [
        "security/ir.model.access.csv",
        "views/hr_payslib_view.xml",
        "views/hr_contract_view.xml",
        "views/hr_salary_rule.xml",
        "views/hr_employee.xml",
        "report/report.xml",
        "report/template_fiche_paie.xml",

    ],
    'assets': {
                
            },
    'post_init_hook': '_post_init_hook',

}
