from odoo import models, fields, api
from datetime import datetime


class DiseaseReport(models.TransientModel):
    _name = 'hr_hospital.disease.report'
    _description = 'Disease Report Wizard'

    date_from = fields.Date(string='From Date', required=True, default=fields.Date.today)
    date_to = fields.Date(string='To Date', required=True, default=fields.Date.today)

    doctor_ids = fields.Many2many(comodel_name='hr_hospital.doctor', string='Doctors')
    disease_ids = fields.Many2many(comodel_name='hr_hospital.disease', string='Diseases')

    diagnosis_ids = fields.Many2many(comodel_name='hr_hospital.diagnosis', string='Diagnoses', compute='_compute_diagnosis_ids')

    @api.depends('date_from', 'date_to', 'doctor_ids', 'disease_ids')
    def _compute_diagnosis_ids(self):
        for wizard in self:
            start_datetime = datetime.combine(wizard.date_from, datetime.min.time())
            end_datetime = datetime.combine(wizard.date_to, datetime.max.time())

            domain = [
                ('visit_id.planned_datetime', '>=', start_datetime),
                ('visit_id.planned_datetime', '<=', end_datetime),
            ]

            if wizard.disease_ids:
                domain.append(('disease_id', 'in', wizard.disease_ids.ids))

            if wizard.doctor_ids:
                domain.append(('visit_id.doctor_id', 'in', wizard.doctor_ids.ids))

            diagnoses = self.env['hr_hospital.diagnosis'].search(domain)
            wizard.diagnosis_ids = diagnoses

    def action_generate_report(self):
        self.ensure_one()
        return {
            'name': 'Disease Report',
            'type': 'ir.actions.act_window',
            'res_model': 'hr_hospital.diagnosis',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.diagnosis_ids.ids)],
            'context': {'create': False},
        }