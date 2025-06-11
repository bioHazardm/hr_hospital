from odoo import models, fields

class Person(models.AbstractModel):
    _name = 'hr_hospital.person'
    _description = 'Abstract Person'

    name = fields.Char(string='First Name', required=True)
    surname = fields.Char(string='Last Name')
    gender = fields.Selection(selection =[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender')
    phone = fields.Char(string='Phone')
    image = fields.Image(string='Photo')
