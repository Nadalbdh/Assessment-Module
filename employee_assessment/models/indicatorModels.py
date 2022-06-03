# -*- coding: utf-8 -*-


from odoo import api, fields, models


class Indicator(models.Model):
    _name = 'assessment.indicator'

    name = fields.Char('Name', required=True)
    seq = fields.Char(copy=False, readonly=True)
    indicatorActive = fields.Boolean('Active', default=True)
    operationalGoal = fields.Many2one('assessment.opgoal', string='Operational Goal')
    indicatorDescription = fields.Text('Description')
    indicatorResponsibleEmployee = fields.Many2one('hr.employee')
    state = fields.Selection([
        ('to be approved', 'To Be Approved'),
        ('approved', 'Approved'),
        ('expired', 'Expired')
    ], string='Status', index=True, default='to be approved',
        track_visibility='onchange', copy=False)
    indicatorImportance = fields.Selection([
        ('0', '0'),
        ('10', '10'),
        ('20', '20'),
        ('30', '30'),
        ('40', '40'),
        ('50', '50'),
        ('60', '60'),
        ('70', '70'),
        ('80', '80'),
        ('90', '90'),
        ('100', '100')
    ], string='Importance')

    measure_ids = fields.One2many('assessment.measure', 'indicator_id', string='Measure Components')
    measure_count = fields.Integer(compute='compute_count_measures')
    risks = fields.One2many('assessment.indicatorrisk', 'indicator')
    progress = fields.Float(compute='_indicator_progress_get', string='Progress', store=True)
    comments = fields.One2many('assessment.indicatorcomment', 'indicator', String="Comments")
    comment_count = fields.Integer(compute='compute_count_comments')
    color = fields.Integer('Kanban Color Index')

    @api.model
    def create(self, vals):
        indicator_no = self.env['ir.sequence'].get('assessment.indicator.seq')
        goal_no = self.env['assessment.opgoal']. \
            browse(vals['operationalGoal']).seq
        vals['seq'] = goal_no + indicator_no
        return super(Indicator, self).create(vals)

    @api.multi
    def compute_count_measures(self):
        for rec in self:
            rec.measure_count = self.env['assessment.measure'].search_count([('indicator_id', '=', rec.id)])

    def compute_count_comments(self):
        for rec in self:
            rec.comment_count = self.env['assessment.indicatorcomment'].search_count([('indicator', '=', rec.id)])

    @api.onchange('operationalGoal')
    def get_dep(self):
        self.indicatorResponsibleEmployee = self.operationalGoal.operationalGoalResponsibleEmployee

    @api.depends('measure_ids.progress')
    def _indicator_progress_get(self):
        for record in self.sorted(key='id', reverse=True):
            somme = 0.0
            if record.measure_count != 0:
                for rec in record.measure_ids:
                    somme += rec.progress
                record.progress = somme / record.measure_count
            else:
                record.progress = 0.0
