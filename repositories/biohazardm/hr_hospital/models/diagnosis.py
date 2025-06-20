from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Diagnosis(models.Model):
    _name = 'hr_hospital.diagnosis'
    _description = 'Patient Diagnosis'

    visit_id = fields.Many2one(
        comodel_name='hr_hospital.visit',
        string='Visit',
        required=True,
        ondelete='cascade'
    )

    disease_id = fields.Many2one(
        comodel_name='hr_hospital.disease',
        string='Disease',
        required=True,
        ondelete='restrict'
    )

    visit_date = fields.Datetime(
        string='Visit Date',
        related='visit_id.planned_datetime',
        store=True,
        readonly=True,
        help='Date of the visit for reporting purposes'
    )

    disease_type_id = fields.Many2one(
        comodel_name='hr_hospital.disease',
        string='Disease Type',
        related='disease_id.parent_id',
        store=True,
        readonly=True,
        help='Type/category of the disease for reporting purposes'
    )

    description = fields.Text('Treatment Notes')

    is_approved = fields.Boolean(
        'Mentor Approval',
        help='Check this when a senior doctor has reviewed and approved an intern\'s diagnosis'
    )

    @api.constrains('is_approved')
    def _check_intern_approval(self):
        for diagnosis in self:
            doctor = diagnosis.visit_id.doctor_id
            if doctor.is_intern and not doctor.mentor_id:
                raise ValidationError(_(
                    "Whoops! This diagnosis was made by an intern (%s) who doesn't have a mentor assigned. "
                    "All interns need a mentor to review their work - please assign one first!"
                ) % doctor.name)
