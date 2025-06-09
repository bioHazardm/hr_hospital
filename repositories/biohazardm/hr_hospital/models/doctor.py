from odoo import models, fields

class Doctor(models.Model):
    _name = 'hr_hospital.doctor'
    _description = 'Hospital Doctor'

    name = fields.Char(string='Name', required=True)
    specialization = fields.Char(string='Specialization')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    active = fields.Boolean(default=True)
    
    patient_ids = fields.One2many(comodel_name='hr_hospital.patient', inverse_name='doctor_id', string='Patients')
    visit_ids = fields.One2many(comodel_name='hr_hospital.visit', inverse_name='doctor_id', string='Visits')
    
    _sql_constraints = [
        ('email_uniq', 'unique(email)', 'Email must be unique!'),
    ]