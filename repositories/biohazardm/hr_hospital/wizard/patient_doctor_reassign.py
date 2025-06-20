from odoo import models, fields, api, _


class PatientDoctorReassign(models.TransientModel):
    _name = 'hr_hospital.patient.doctor.reassign'
    _description = 'Change Doctor for Multiple Patients'

    doctor_id = fields.Many2one(
        comodel_name='hr_hospital.doctor',
        string='New Doctor', 
        required=True,
        help='The doctor who will take over care for the selected patients'
    )


    def action_reassign_doctor(self):
        selected_patients = self._get_selected_patients()

        if selected_patients:
            selected_patients.write({
                'doctor_id': self.doctor_id.id
            })
        return {'type': 'ir.actions.act_window_close'}

    def _get_selected_patients(self):
        patient_ids = self.env.context.get('active_ids', [])
        return self.env['hr_hospital.patient'].browse(patient_ids)
