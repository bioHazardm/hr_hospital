from odoo import models, fields, _  # Added translation support


class Specialization(models.Model):
    """Medical specializations for doctors.

    Examples: Cardiology, Neurology, Pediatrics, etc."""
    _name = 'hr_hospital.specialization'
    _description = 'Medical Specialization'
    _order = 'name'  # Alphabetical order makes sense here

    name = fields.Char('Name', required=True)  # Simplified - no string=
    description = fields.Text('Description')  # What this specialization covers
    active = fields.Boolean(default=True)  # For archiving old specializations


    _sql_constraints = [
        # Can't have duplicate specializations - would be confusing!
        ('name_uniq', 'unique(name)', 
         _("This specialization already exists! Please pick a different name or use the existing one.")),
    ]
