from odoo import models, api, fields
from datetime import datetime, date


class ProjectReportParser(models.AbstractModel):
    _name = 'report.hr_payroll_community.report_synthese_payslip_view'
    _description = 'Report Hr Payroll Report Synthese Payslip'

    @api.model
    def _get_report_values(self, docids, data=None):
        company_id = self.env.company

        start_date = data.get('start_date')
        end_date = data.get('end_date')

        all_payslip = self.env['hr.payslip'].search([
            ('date_from', '>=', start_date),
            ('date_to', '<=', end_date)])
        taille = 4
        liste_dico = [all_payslip[i:i + taille] for i in range(0, len(all_payslip), taille)]

        salaire_base = 0
        sur_salaire = 0
        net_pay = 0
        total_journalier = 0
        responsability_bonus = 0
        pa = 0
        taxable_transportation_allowance = 0
        prime_salissure_imposable = 0
        gratification = 0
        mount_15 = 0
        mount_50 = 0
        mount_75 = 0
        mount_100 = 0
        basket_bonus = 0
        Licensing_compensation = 0
        paid_vacation = 0
        indemnite_depart_retraite = 0
        brut = 0
        ist = 0
        cn = 0
        igr = 0
        cmu = 0
        cnps = 0
        retraite_generale = 0
        prestation_familiale = 0
        assurance_maternite = 0
        work_related_accident = 0
        taxe_app = 0
        taxe_fpc = 0
        total_cotisation = 0
        transport = 0
        exceptionnelle = 0
        rendement = 0
        advantage_in_kind = 0
        other_bonus = 0
        rappel_salaire = 0
        indemnite_licencement_non_imp = 0
        retenu_absence = 0
        Acompte = 0
        salary_advance = 0

        for payslip in all_payslip:
            print("allll", payslip)
            brut += payslip.wage
            salaire_base += payslip.contract_id.salary
            sur_salaire += payslip.contract_id.su_salary
            total_journalier += payslip.contract_id.daily_pay
            responsability_bonus += payslip.responsibility_bonus
            pa += payslip.contract_id.seniority_bonus
            taxable_transportation_allowance += payslip.contract_id.taxable_transportation_allowance
            prime_salissure_imposable += payslip.prime_salissure_imposable
            gratification += payslip.contract_id.gratification
            mount_15 += payslip.mount_15
            mount_50 += payslip.mount_50
            mount_75 += payslip.mount_75
            mount_100 += payslip.mount_100
            basket_bonus += payslip.basket_bonus
            Licensing_compensation += payslip.contract_id.Licensing_compensation
            paid_vacation += payslip.contract_id.paid_vacation
            indemnite_depart_retraite += payslip.contract_id.indemnite_depart_retraite
            ist += payslip.wage_salary_tax
            cn += payslip.national_contribution
            igr += payslip.general_income_tax
            cnps += payslip.cnps_salariale
            retraite_generale += payslip.general_retirement
            prestation_familiale += payslip.family_benefit
            assurance_maternite += payslip.maternity_insurance
            work_related_accident += payslip.work_related_accident
            taxe_app += payslip.applicable_taxe
            taxe_fpc += payslip.taxe_fpc
            total_cotisation += payslip.total_contribution
            transport += payslip.travel_allowance
            exceptionnelle += payslip.exceptional_bonus
            rendement += payslip.performance_bonus
            advantage_in_kind += payslip.advantage_in_kind
            other_bonus += payslip.other_bonus
            rappel_salaire += payslip.contract_id.monthly_salary_recall
            # round += payslip.contract_id.round
            indemnite_licencement_non_imp += payslip.contract_id.indemnite_licencement
            retenu_absence += payslip.retenu_absence
            Acompte += payslip.acompte
            salary_advance += payslip.salary_advance
            net_pay += payslip.net_pay
            cmu += payslip.cmu

        datas = {
            'brut': brut,
            'salaire_base': salaire_base,
            'sur_salaire': sur_salaire,
            'net_pay': net_pay,
            'total_journalier': total_journalier,
            'responsability_bonus': responsability_bonus,
            'pa': pa,
            'taxable_transportation_allowance': taxable_transportation_allowance,
            'prime_salissure_imposable': prime_salissure_imposable,
            'gratification': gratification,
            'mount_15': mount_15,
            'mount_50': mount_50,
            'mount_75': mount_75,
            'mount_100': mount_100,
            'basket_bonus': basket_bonus,
            'Licensing_compensation': Licensing_compensation,
            'paid_vacation': paid_vacation,
            'indemnite_depart_retraite': indemnite_depart_retraite,
            'ist': ist,
            'cn': cn,
            'igr': igr,
            'cnps': cnps,
            'retraite_generale': retraite_generale,
            'prestation_familiale': prestation_familiale,
            'assurance_maternite': assurance_maternite,
            'work_related_accident': work_related_accident,
            'taxe_app': taxe_app,
            'taxe_fpc': taxe_fpc,
            'total_cotisation': total_cotisation,
            'transport': transport,
            'exceptionnelle': exceptionnelle,
            'rendement': rendement,
            'advantage_in_kind': advantage_in_kind,
            'other_bonus': other_bonus,
            'retenu_absence': retenu_absence,
            'Acompte': Acompte,
            'rappel_salaire': rappel_salaire,
            'indemnite_licencement_non_imp': indemnite_licencement_non_imp,
            'salary_advance': salary_advance,
            'cmu': cmu,
            'company_id': company_id,
        }
        date_of_day = date.today()
        now = datetime.now()
        current_time = now.strftime("%H:%M")

        return {
            "doc_model": 'hr.payslip',
            'docs': liste_dico,
            'start_date': start_date,
            'end_date': end_date,
            'date_of_day': date_of_day,
            'now': current_time,
            'datas': datas,
            'report_type': data.get('report_type') if data else '',
        }
