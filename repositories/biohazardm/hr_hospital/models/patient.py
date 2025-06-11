from odoo import models, fields, api, _  # Don't forget translations
from datetime import date

from odoo.exceptions import ValidationError


class Patient(models.Model):
    # Patient model - inherits basic info from person
    _name = 'hr_hospital.patient'
    _inherit = 'hr_hospital.person'
    _description = 'Hospital Patient'

    # Basic patient info
    birthday = fields.Date(string='Date of Birth')  # Used to calculate age
    age = fields.Integer(string='Age', compute='_compute_age', store=True)  # Stored for performance

    # ID and emergency info
    passport = fields.Char(string='Passport Number')  # For identification
    emergency_contact = fields.Char('Emergency Contact')  # Simplified - no string= needed

    personal_doctor_id = fields.Many2one(comodel_name='hr_hospital.doctor', string='Primary Care Doctor')

    # Contact details
    email = fields.Char('Email Address')  # Changed label slightly
    address = fields.Text('Home Address')  # Changed label slightly
    active = fields.Boolean(default=True)  # For archiving

    # This seems redundant with personal_doctor_id - need to check with the team
    doctor_id = fields.Many2one(comodel_name='hr_hospital.doctor', string='Doctor')
    # Patient's visit history
    visit_ids = fields.One2many(comodel_name='hr_hospital.visit', inverse_name='patient_id', string='Visit History')

    # Prevent duplicate emails - important for patient portal access
    _sql_constraints = [
        ('email_uniq', 'unique(email)',
         "This email is already registered! Each patient needs their own email address."),
    ]

    @api.depends('birthday')
    def _compute_age(self):
        """Calculate patient age based on birthday.
        Uses the more accurate approach that accounts for leap years and actual birth date."""
        today = date.today()  # Get current date once for all records

        for patient in self:
            if not patient.birthday:
                patient.age = 0  # No birthday, no age!
                continue

            # This formula accounts for leap years correctly
            patient.age = today.year - patient.birthday.year - (
                    (today.month, today.day) < (patient.birthday.month, patient.birthday.day)
            )

    def write(self, vals):
        # Prevent changing key fields for completed visits
        if any(visit.state == 'done' for visit in self):
            no_change_fields = {'planned_datetime', 'doctor_id', 'patient_id'}
            if no_change_fields & set(vals.keys()):
                raise ValidationError(
                    _("Sorry! You can't change the doctor, patient, or date once a visit is completed. Hospital regulations!"))

        # Check if the state is being changed to 'done'
        if vals.get('state') == 'done':
            # For each visit being updated
            for visit in self:
                # Only update if the visit wasn't already completed
                if visit.state != 'done':
                    # Update the patient's personal doctor to the visit's doctor
                    visit.patient_id.write({
                        'personal_doctor_id': visit.doctor_id.id
                    })
                    # You could also add a nice log message here
                    visit.message_post(
                        body=_("Dr. %s has been set as %s's primary care doctor.") %
                             (visit.doctor_id.name, visit.patient_id.name)
                    )

        return super().write(vals)
