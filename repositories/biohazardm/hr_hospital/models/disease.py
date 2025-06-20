from odoo import models, fields, _


class Disease(models.Model):
    _name = 'hr_hospital.disease'
    _description = 'Medical Condition'
    _order = 'name'

    # Basic info
    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    symptoms = fields.Text('Common Symptoms')
    treatment = fields.Text('Standard Treatment')
    active = fields.Boolean(default=True)

    parent_id = fields.Many2one(comodel_name='hr_hospital.disease', string='Parent Category')
    child_ids = fields.One2many(comodel_name='hr_hospital.disease', inverse_name='parent_id', string='Subcategories')
    parent_path = fields.Char(index=True)

    _parent_name = 'parent_id'
    _parent_store = True

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 
         _("This disease is already in our database! Please use the existing record or choose a more specific name.")),
    ]
