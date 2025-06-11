from odoo import models, fields, api, _  # Added _ for translations
from odoo.exceptions import ValidationError


class Doctor(models.Model):
    # Doctors inherit from person and add medical-specific fields
    _name = 'hr_hospital.doctor'
    _inherit = 'hr_hospital.person'
    _description = 'Hospital Doctor'

    # Medical qualifications
    specialization_id = fields.Many2one(comodel_name='hr_hospital.specialization', string='Specialization')
    is_intern = fields.Boolean(string='Is Intern')
    # Make sure mentors aren't interns themselves - that would be crazy!
    mentor_id = fields.Many2one(comodel_name='hr_hospital.doctor', string='Mentor',
                               domain="[('is_intern', '=', False)]")

    # Contact info - might move this to person model later if needed for patients too
    email = fields.Char(string='Email')
    active = fields.Boolean(default=True)  # for archiving

    # Relationships
    patient_ids = fields.One2many(comodel_name='hr_hospital.patient', inverse_name='doctor_id', string='Patients')
    visit_ids = fields.One2many(comodel_name='hr_hospital.visit', inverse_name='doctor_id', string='Visits')


    # Make sure emails don't get duplicated
    _sql_constraints = [
        ('email_uniq', 'unique(email)', "Hey, this email is already used by another doctor!"),
    ]

    @api.constrains('mentor_id')
    def _check_mentor_is_not_intern(self):
        # Double-check that no one assigned an intern as mentor
        for doctor in self:
            if doctor.mentor_id and doctor.mentor_id.is_intern:
                raise ValidationError(_("Come on! An intern can't be a mentor. That's like asking a student to teach the class!"))
