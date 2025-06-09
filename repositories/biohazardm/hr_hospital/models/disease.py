from odoo import models, fields

class Disease(models.Model):
    _name = 'hr_hospital.disease'
    _description = 'Disease'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    symptoms = fields.Text(string='Symptoms')
    treatment = fields.Text(string='Treatment')
    active = fields.Boolean(default=True)
    
    visit_ids = fields.One2many('hr_hospital.visit', 'disease_id', string='Visits')
    
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Disease name must be unique!'),
    ]