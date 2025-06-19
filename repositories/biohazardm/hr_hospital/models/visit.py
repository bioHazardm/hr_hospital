from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
# Importing what we need for the visit model

class Visit(models.Model):
    # Main model for tracking patient visits to doctors
    _name = 'hr_hospital.visit'
    _description = 'Patient Visit'
    _order = 'planned_datetime desc, id desc'  # newest visits first

    # Visit reference - auto-generated
    name = fields.Char(string='Reference', required=True, copy=False, readonly=True,
                      default=lambda self: _('New'))  # will be replaced by sequence

    # The main fields we need for any visit
    patient_id = fields.Many2one(comodel_name='hr_hospital.patient', string='Patient', required=True)
    doctor_id = fields.Many2one(comodel_name='hr_hospital.doctor', string='Doctor', required=True)

    # When the visit is scheduled vs when it actually happened
    planned_datetime = fields.Datetime(string='Planned Date & Time', required=True)
    actual_datetime = fields.Datetime(string='Actual Visit Time')  # filled when visit is done

    # Visit status tracking
    state = fields.Selection([
        ('planned', 'Planned'),
        ('done', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='planned')  # all visits start as planned

    # For archiving
    active = fields.Boolean(default=True)

    # Related diagnoses - one visit can have multiple diagnoses
    diagnosis_ids = fields.One2many(comodel_name='hr_hospital.diagnosis', inverse_name='visit_id', string='Diagnoses')

    # Free text fields for doctor notes
    description = fields.Text(string='Description')
    prescription = fields.Text(string='Prescription')

    @api.model_create_multi
    def create(self, vals_list):
        # Generate sequence number for new visits
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('hr_hospital.visit') or _('New')
        return super().create(vals_list)

    def write(self, vals):
        # Prevent changing key fields for completed visits
        if any(visit.state == 'done' for visit in self):
            no_change_fields = {'planned_datetime', 'doctor_id', 'patient_id'}
            if no_change_fields & set(vals.keys()):
                raise ValidationError(_("Sorry! You can't change the doctor, patient, or date once a visit is completed. Hospital regulations!"))
        return super().write(vals)

    def unlink(self):
        # Don't allow deleting visits with diagnoses
        for visit in self:
            if visit.diagnosis_ids:
                raise ValidationError(_("Oops! Can't delete this visit because it has diagnoses attached. Remove those first."))
        return super().unlink()

    def toggle_active(self):
        # Same logic for archiving - can't archive with diagnoses
        for visit in self:
            if visit.diagnosis_ids:
                raise ValidationError(_("Can't archive this visit while it has diagnoses. Please deal with the diagnoses first!"))
        return super().toggle_active()

    @api.constrains('patient_id', 'doctor_id', 'planned_datetime')
    def _check_duplicate_visit(self):
        # Make sure we don't double-book
        for visit in self:
            if visit.patient_id and visit.doctor_id and visit.planned_datetime:
                # Get full day range
                day_start = visit.planned_datetime.replace(hour=0, minute=0, second=0)
                day_end = visit.planned_datetime.replace(hour=23, minute=59, second=59)

                # Check for other visits same day, same doctor, same patient
                same_day_visits = [
                    ('id', '!=', visit.id),
                    ('patient_id', '=', visit.patient_id.id),
                    ('doctor_id', '=', visit.doctor_id.id),
                    ('planned_datetime', '>=', day_start),
                    ('planned_datetime', '<=', day_end),
                    ('state', '!=', 'cancelled')
                ]

                if self.search_count(same_day_visits):
                    raise ValidationError(_("This patient already has an appointment with Dr. %s on this day. Please choose another day or doctor!") % visit.doctor_id.name)
