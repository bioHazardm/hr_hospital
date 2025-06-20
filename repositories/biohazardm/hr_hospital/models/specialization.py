from odoo import models, fields, _


class Specialization(models.Model):
    _name = 'hr_hospital.specialization'
    _description = 'Medical Specialization'
    _order = 'name'

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    active = fields.Boolean(default=True)


    _sql_constraints = [
        ('name_uniq', 'unique(name)', 
         _("This specialization already exists! Please pick a different name or use the existing one.")),
    ]
