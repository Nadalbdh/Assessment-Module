# -*- coding: utf-8 -*-


from odoo import api, fields, models


class Award(models.Model):
    _name = 'assessment.award'

    name = fields.Char(string='Name', required=True)
    seq = fields.Char(readonly=True, copy=False)
    date_from = fields.Datetime(string="From", default=fields.Datetime.now, required=True)
    date_to = fields.Datetime(string="To", required=True)
    awardActive = fields.Boolean('Active', default=True, required=True)
    awardVision = fields.Text('Vision', required=True)
    awardDescription = fields.Text('Specific Targets', required=True)
    awardValues = fields.Text('Values')
    state = fields.Selection([
        ('to be approved', 'To Be Approved'),
        ('approved', 'Approved'),
        ('expired', 'Expired')
    ], string='Status', index=True, default='to be approved',
        track_visibility='onchange', copy=False, store=True)

    awardDepartment = fields.Many2one('hr.department', string='Department', required=True)
    comments = fields.One2many('assessment.awardcomment', 'award', String="Comments")
    comment_count = fields.Integer(compute='compute_count_comments')
    strategicGoals = fields.One2many('assessment.stgoal', 'relatedAward', string='Strategic Goals')
    stgoal_count = fields.Integer(compute='_compute_count_st_goals')
    color = fields.Integer('Kanban Color Index')
    progress = fields.Float(compute='_award_progress_get', string='Progress', store=True)

    @api.model
    def create(self, vals):
        vals['seq'] = self.env['ir.sequence'].next_by_code('code')
        return super(Award, self).create(vals)

    @api.multi
    def _compute_count_st_goals(self):
        for rec in self:
            rec.stgoal_count = self.env['assessment.stgoal'].search_count([('relatedAward', '=', rec.id)])

    @api.multi
    def compute_count_comments(self):
        for rec in self:
            rec.comment_count = self.env['assessment.awardcomment'].search_count([('award', '=', rec.id)])

    @api.depends('strategicGoals.progress')
    def _award_progress_get(self):
        for record in self:
            if record.stgoal_count != 0:
                somme = 0.0
                for rec in record.strategicGoals:
                    somme += rec.progress
                record.progress = somme / record.stgoal_count
            else:
                record.progress = 0.0
