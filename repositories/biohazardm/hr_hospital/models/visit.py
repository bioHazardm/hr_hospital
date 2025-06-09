from odoo import models, fields, api, _


class Visit(models.Model):
    _name = 'hr_hospital.visit'
    _description = 'Patient Visit'
    _order = 'date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, 
                       default=lambda self: _('New'))
    patient_id = fields.Many2one('hr_hospital.patient', string='Patient', required=True)
    doctor_id = fields.Many2one('hr_hospital.doctor', string='Doctor', required=True)
    disease_id = fields.Many2one('hr_hospital.disease', string='Disease')
    date = fields.Datetime(string='Visit Date', default=fields.Datetime.now)
    description = fields.Text(string='Description')
    prescription = fields.Text(string='Prescription')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft')
    active = fields.Boolean(default=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hr_hospital.visit') or _('New')
        return super(Visit, self).create(vals)

    def action_confirm(self):
        for record in self:
            record.state = 'confirmed'

    def action_done(self):
        for record in self:
            record.state = 'done'

    def action_cancel(self):
        for record in self:
            record.state = 'cancelled'

    def action_draft(self):
        for record in self:
            record.state = 'draft'
