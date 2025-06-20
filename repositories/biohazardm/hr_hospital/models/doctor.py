from odoo import models, fields, api, _  # Added _ for translations
from odoo.exceptions import ValidationError


class Doctor(models.Model):
    _name = 'hr_hospital.doctor'
    _inherit = 'hr_hospital.person'
    _description = 'Hospital Doctor'

    specialization_id = fields.Many2one(comodel_name='hr_hospital.specialization', string='Specialization')
    is_intern = fields.Boolean(string='Is Intern')
    mentor_id = fields.Many2one(comodel_name='hr_hospital.doctor', string='Mentor',
                               domain="[('is_intern', '=', False)]")

    intern_ids = fields.One2many(comodel_name='hr_hospital.doctor', inverse_name='mentor_id', string='Interns')

    email = fields.Char(string='Email')
    active = fields.Boolean(default=True)

    patient_ids = fields.One2many(comodel_name='hr_hospital.patient', inverse_name='doctor_id', string='Patients')
    visit_ids = fields.One2many(comodel_name='hr_hospital.visit', inverse_name='doctor_id', string='Visits')


    _sql_constraints = [
        ('email_uniq', 'unique(email)', "Hey, this email is already used by another doctor!"),
    ]

    @api.constrains('mentor_id')
    def _check_mentor_is_not_intern(self):
        for doctor in self:
            if doctor.mentor_id and doctor.mentor_id.is_intern:
                raise ValidationError(_("Come on! An intern can't be a mentor. That's like asking a student to teach the class!"))
