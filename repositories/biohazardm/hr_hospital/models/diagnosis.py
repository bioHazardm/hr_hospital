from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Diagnosis(models.Model):
    """Links diseases to patient visits with treatment details.
    Also handles the approval workflow for diagnoses made by interns."""
    _name = 'hr_hospital.diagnosis'
    _description = 'Patient Diagnosis'  # More descriptive

    # Link to the visit - if visit is deleted, delete the diagnosis too
    visit_id = fields.Many2one(
        comodel_name='hr_hospital.visit',
        string='Visit',
        required=True,
        ondelete='cascade'  # If visit is deleted, diagnosis goes too
    )

    # The actual disease being diagnosed
    # Can't delete diseases that are used in diagnoses
    disease_id = fields.Many2one(
        'hr_hospital.disease',
        string='Disease',
        required=True,
        ondelete='restrict'  # Can't delete diseases used in diagnoses
    )

    # Doctor's notes on treatment
    description = fields.Text('Treatment Notes')

    # For intern approval workflow
    is_approved = fields.Boolean(
        'Mentor Approval',
        help='Check this when a senior doctor has reviewed and approved an intern\'s diagnosis'
    )

    @api.constrains('is_approved')
    def _check_intern_approval(self):
        """Make sure interns have mentors to approve their work.
        Hospital policy requires all intern diagnoses to be reviewed."""
        for diagnosis in self:
            doctor = diagnosis.visit_id.doctor_id
            if doctor.is_intern and not doctor.mentor_id:
                raise ValidationError(_(
                    "Whoops! This diagnosis was made by an intern (%s) who doesn't have a mentor assigned. "
                    "All interns need a mentor to review their work - please assign one first!"
                ) % doctor.name)
