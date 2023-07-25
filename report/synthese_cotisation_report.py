from odoo import models, api, fields
from datetime import datetime, date


class ReportParser(models.AbstractModel):
    _name = 'report.hr_payroll_community.fiche_report_cotisation'
    _description = 'Report Hr Payroll Fiche Report Cotisation'

    @api.model
    def _get_report_values(self, docids, data=None):
        print("cotisation%%%%")
        company_id = self.env.company
        print(company_id)
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        print("date", start_date)
        all_payslip = self.env['hr.payslip'].search([
            ('date_from', '>=', start_date),
            ('date_to', '<=', end_date)])
        salaire_base = 0
        sur_salaire = 0
        net_pay = 0
        responsability_bonus = 0
        brut = 0
        ist = 0
        cn = 0
        igr = 0
        cmu = 0
        cnps = 0
        cotisation = 0
        transport = 0
        exceptionnelle = 0
        rendement = 0
        taxe_app = 0
        taxe_fpc = 0
        cnps_salariale = 0
        prestation_familiale = 0
        taux_work_related_accident = 0
        advantage_in_kind = 0
        exceptional_bonus = 0
        performance_bonus = 0
        pf = 0
        at = 0
        male = 0
        female = 0
        matricule = []
        for payslip in all_payslip:
            brut += payslip.wage
            salaire_base += payslip.contract_id.salary
            sur_salaire += payslip.contract_id.su_salary
            responsability_bonus += payslip.responsibility_bonus
            ist += payslip.wage_salary_tax
            cn += payslip.national_contribution
            igr += payslip.general_income_tax
            cnps += payslip.cnps_salariale
            advantage_in_kind += payslip.advantage_in_kind
            exceptional_bonus += payslip.exceptional_bonus
            performance_bonus += payslip.performance_bonus
            cotisation += payslip.wage_salary_tax
            cotisation += payslip.national_contribution
            cotisation += payslip.general_income_tax
            cotisation += payslip.cnps_salariale
            transport += payslip.travel_allowance
            # exceptionnelle += payslip.contract_id.exceptional_bonus
            rendement += payslip.performance_bonus
            net_pay += payslip.net_pay
            cmu += payslip.cmu
            taxe_app += payslip.applicable_taxe
            taxe_fpc += payslip.taxe_fpc
            cnps_salariale += payslip.cnps_salariale
            prestation_familiale += payslip.family_benefit
            taux_work_related_accident = payslip.company_id.work_accident_rate
            pf += 70000
            at += 70000
            matricule.append(payslip.employee_id.personnel_number)

        employees = self.env['hr.employee'].search([])
        for employee in employees:
            if employee.gender:
                if employee.gender == 'male':
                    male += 1
                if employee.gender == 'female':
                    female += 1
        datas = {
            'brut': brut,
            'salaire_base': salaire_base,
            'sur_salaire': sur_salaire,
            'net_pay': net_pay,
            'responsability_bonus': responsability_bonus,
            'ist': ist,
            'cn': cn,
            'igr': igr,
            'cnps': cnps,
            'cotisation': cotisation,
            'transport': transport,
            'exceptionnelle': exceptionnelle,
            'rendement': rendement,
            'cmu': cmu,
            'company_id': company_id,
            'taxe_app': taxe_app,
            'taxe_fpc': taxe_fpc,
            'pf': pf,
            'at': at,
            'taux_work_related_accident': taux_work_related_accident,
            'male': male,
            'female': female,
            'matricule': matricule,
            'advantage_in_kind': advantage_in_kind,
            'exceptional_bonus': exceptional_bonus,
            'performance_bonus': performance_bonus
        }
        date_of_day = date.today()
        now = datetime.now()
        current_time = now.strftime("%H:%M")

        return {
            "doc_model": 'hr.payslip',
            'docs': all_payslip,
            'start_date': start_date,
            'end_date': end_date,
            'date_of_day': date_of_day,
            'now': current_time,
            'datas': datas,
            'report_type': data.get('report_type') if data else '',
        }
