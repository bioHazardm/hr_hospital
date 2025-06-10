from odoo import models, fields

class Patient(models.Model):
    _name = 'hr_hospital.patient'
    _description = 'Hospital Patient'

    name = fields.Char(string='Name', required=True)
    date_of_birth = fields.Date(string='Date of Birth')
    gender = fields.Selection(
        selection=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    address = fields.Text(string='Address')
    active = fields.Boolean(default=True)
    
    doctor_id = fields.Many2one(comodel_name='hr_hospital.doctor', string='Doctor')
    visit_ids = fields.One2many(comodel_name='hr_hospital.visit', inverse_name='patient_id', string='Visits')
    
    _sql_constraints = [
        ('email_uniq', 'unique(email)', 'Email must be unique!'),
    ]