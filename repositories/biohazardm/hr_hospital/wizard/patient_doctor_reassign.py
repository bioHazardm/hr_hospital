from odoo import models, fields, api, _


class PatientDoctorReassign(models.TransientModel):
    """Bulk reassignment wizard for patients' doctors.

    This saves a ton of time when a doctor leaves or when we need to
    redistribute patient load between doctors."""
    _name = 'hr_hospital.patient.doctor.reassign'
    _description = 'Change Doctor for Multiple Patients'  # More descriptive

    # The doctor we're assigning to the selected patients
    doctor_id = fields.Many2one(
        comodel_name='hr_hospital.doctor',
        string='New Doctor', 
        required=True,
        help='The doctor who will take over care for the selected patients'
    )


    def action_reassign_doctor(self):
        """Assign the selected doctor to all selected patients.
        Updates the doctor_id field on all patients."""
        # Get the patients selected in the UI
        selected_patients = self._get_selected_patients()

        if selected_patients:
            # Do the actual reassignment
            selected_patients.write({
                'doctor_id': self.doctor_id.id
            })

            # Could add a nice message here in the future

        # Close the wizard
        return {'type': 'ir.actions.act_window_close'}

    def _get_selected_patients(self):
        """Helper to get the patients selected in the UI."""
        patient_ids = self.env.context.get('active_ids', [])
        return self.env['hr_hospital.patient'].browse(patient_ids)
