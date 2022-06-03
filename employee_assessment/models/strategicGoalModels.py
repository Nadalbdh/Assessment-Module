# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions


class StrategicGoal(models.Model):
    _name = 'assessment.stgoal'

    name = fields.Char('Name', required=True)
    seq = fields.Char(copy=False, readonly=True)
    date_to = fields.Datetime(string="To", required=True)
    strategicGoalActive = fields.Boolean('Active', default=True)
    strategicGoalDescription = fields.Text('Description', required=True)
    strategicGoalDepartment = fields.Many2one('hr.department', string='Department')
    strategicGoalResponsibleEmployee = fields.Many2one('hr.employee', string='Manager')
    relatedAward = fields.Many2one('assessment.award', string="Award")
    strategicGoalImportance = fields.Selection([
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
    strategicRelations = fields.One2many('assessment.relation', 'related_strategical_goal')
    successFactors = fields.One2many('assessment.success', 'related_strategical_goal')
    operationalGoals = fields.One2many('assessment.opgoal', 'relatedStrategicGoal',
                                       string='Operational Goals')
    comments = fields.One2many('assessment.stgoalcomment', 'strategicGoal', String="Comments")
    comment_count = fields.Integer(compute='compute_count_comments')
    opgoal_count = fields.Integer(compute='compute_count_op_goals')
    color = fields.Integer('Kanban Color Index')
    risks = fields.One2many('assessment.stgoalrisk', 'strategicGoal')
    progress = fields.Float(compute='_stgoal_progress_get', string='Progress', store=True)

    @api.model
    def create(self, vals):
        goal_no = self.env['ir.sequence'].get('assessment.stgoal.seq')
        award_no = self.env['assessment.award']. \
            browse(vals['relatedAward']).seq
        vals['seq'] = str(award_no) + str(goal_no)
        return super(StrategicGoal, self).create(vals)

    @api.multi
    def compute_count_op_goals(self):
        for rec in self:
            rec.opgoal_count = self.env['assessment.opgoal'].search_count([('relatedStrategicGoal', '=', rec.id)])

    def compute_count_comments(self):
        for rec in self:
            rec.comment_count = self.env['assessment.stgoalcomment'].search_count([('strategicGoal', '=', rec.id)])

    @api.depends('operationalGoals.progress')
    def _stgoal_progress_get(self):
        for record in self.sorted(key='id', reverse=True):
            somme = 0.0
            if record.opgoal_count != 0:
                for rec in record.operationalGoals:
                    somme += rec.progress
                record.progress = somme / record.opgoal_count
            else:
                record.progress = 0.0

    @api.onchange('relatedAward')
    def get_dep(self):
        self.strategicGoalDepartment = self.relatedAward.awardDepartment

    @api.onchange('strategicGoalDepartment')
    def get_manager(self):
        self.strategicGoalResponsibleEmployee = self.strategicGoalDepartment.manager_id


class StrategicalRelation(models.Model):
    _name = 'assessment.relation'

    name = fields.Char('Strategical Relation')
    strategicalRelationDescription = fields.Text('Description')
    strategicalRelationDegree = fields.Integer('Degree')
    related_strategical_goal = fields.Many2one('assessment.stgoal', string="related_goal")
    related_operational_goal = fields.Many2one('assessment.opgoal', string="related_goal")


class SuccessFactor(models.Model):
    _name = 'assessment.success'

    name = fields.Char('Success Factor')
    related_strategical_goal = fields.Many2one('assessment.stgoal', string="related_goal")


