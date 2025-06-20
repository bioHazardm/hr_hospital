from odoo import models, fields, api, _
from datetime import date

from odoo.exceptions import ValidationError


class Patient(models.Model):
    _name = 'hr_hospital.patient'
    _inherit = 'hr_hospital.person'
    _description = 'Hospital Patient'

    birthday = fields.Date(string='Date of Birth')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)

    passport = fields.Char(string='Passport Number')
    emergency_contact = fields.Char('Emergency Contact')

    email = fields.Char('Email Address')
    address = fields.Text('Home Address')
    active = fields.Boolean(default=True)

    doctor_id = fields.Many2one(comodel_name='hr_hospital.doctor', string='Doctor')
    visit_ids = fields.One2many(comodel_name='hr_hospital.visit', inverse_name='patient_id', string='Visit History')

    diagnosis_history = fields.One2many(comodel_name='hr_hospital.diagnosis', compute='_compute_diagnosis_history',
                                        string='Diagnosis History')

    _sql_constraints = [
        ('email_uniq', 'unique(email)',
         "This email is already registered! Each patient needs their own email address."),
    ]

    @api.depends('birthday')
    def _compute_age(self):
        today = date.today()

        for patient in self:
            if not patient.birthday:
                patient.age = 0
                continue

            patient.age = today.year - patient.birthday.year - (
                    (today.month, today.day) < (patient.birthday.month, patient.birthday.day)
            )

    @api.depends('visit_ids', 'visit_ids.diagnosis_ids')
    def _compute_diagnosis_history(self):
        for patient in self:
            visit_ids = patient.visit_ids.ids
            diagnoses = self.env['hr_hospital.diagnosis'].search([
                ('visit_id', 'in', visit_ids)
            ])

            patient.diagnosis_history = diagnoses

    def write(self, vals):
        for patient in self:
            if any(visit.state == 'done' for visit in patient.visit_ids):
                no_change_fields = {'planned_datetime', 'doctor_id', 'patient_id'}
                if no_change_fields & set(vals.keys()):
                    raise ValidationError(
                        _("Sorry! You can't change the doctor, patient, or date once a visit is completed. Hospital regulations!"))

        if vals.get('state') == 'done':
            for visit in self:
                if visit.state != 'done':
                    visit.patient_id.write({
                        'doctor_id': visit.doctor_id.id
                    })
                    visit.message_post(
                        body=_("Dr. %s has been set as %s's doctor.") %
                             (visit.doctor_id.name, visit.patient_id.name)
                    )

        return super().write(vals)
