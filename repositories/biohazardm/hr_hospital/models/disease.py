from odoo import models, fields, _


class Disease(models.Model):
    """Medical conditions that can be diagnosed.

    Organized in a hierarchical structure so we can group related diseases.
    For example: Respiratory Diseases > Pneumonia > Bacterial Pneumonia"""
    _name = 'hr_hospital.disease'
    _description = 'Medical Condition'
    _order = 'name'  # Alphabetical makes it easier to find

    # Basic info
    name = fields.Char('Name', required=True)  # Simplified
    description = fields.Text('Description')  # General info about the disease
    symptoms = fields.Text('Common Symptoms')  # Changed label slightly
    treatment = fields.Text('Standard Treatment')  # Changed label slightly
    active = fields.Boolean(default=True)  # For archiving

    # Hierarchical structure - allows grouping diseases
    # (e.g., Cardiovascular > Arrhythmia > Atrial Fibrillation)
    parent_id = fields.Many2one('hr_hospital.disease', string='Parent Category')
    child_ids = fields.One2many('hr_hospital.disease', 'parent_id', string='Subcategories')
    parent_path = fields.Char(index=True)  # Technical field for hierarchy

    # Technical fields for hierarchy
    _parent_name = 'parent_id'
    _parent_store = True  # Enables efficient hierarchical queries

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 
         _("This disease is already in our database! Please use the existing record or choose a more specific name.")),
    ]
