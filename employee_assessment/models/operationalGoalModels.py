# -*- coding: utf-8 -*-


from odoo import api, fields, models, exceptions


class OperationalGoal(models.Model):
    _name = 'assessment.opgoal'

    name = fields.Char('Name', required=True)
    seq = fields.Char(copy=False, readonly=True)
    operationalGoalActive = fields.Boolean('Active', default=True)
    operationalGoalDescription = fields.Text('Description', required=True)
    operationalGoalDepartment = fields.Many2one('hr.department', string='Department', required=True)
    operationalGoalResponsibleEmployee = fields.Many2one('hr.employee', string='Manager')
    relatedStrategicGoal = fields.Many2one('assessment.stgoal', string="Strategic Goal")
    operationalGoalImportance = fields.Selection([
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
    ], string='Importance', groups='hr.group_hr_user')
    strategicRelations = fields.One2many('assessment.relation', 'related_operational_goal',
                                         string='Strategical Relations')
    date_from = fields.Datetime(string="From", default=fields.Datetime.now, required=True)
    date_to = fields.Datetime(string="To", required=True)
    budget = fields.Float('Budget')
    currency_id = fields.Many2one('res.currency', string='Currency')
    comments = fields.One2many('assessment.opgoalcomment', 'operationalGoal', String="Comments")
    comment_count = fields.Integer(compute='compute_count_comments')
    projects = fields.One2many('project.project', 'relatedOperationalGoal', string="Related Projects")
    project_count = fields.Integer(compute='compute_count_projects')
    progress = fields.Float(compute='_opgoal_progress_get', string='Progress', store=True)
    color = fields.Integer('Kanban Color Index ')
    risks = fields.One2many('assessment.opgoalrisk', 'operationalGoal')
    indicator_ids = fields.One2many('assessment.indicator', 'operationalGoal')
    indicator_count = fields.Integer(compute='compute_count_indicator')
    somme = fields.Float()

    @api.model
    def create(self, vals):
        opgoal_no = self.env['ir.sequence'].get('assessment.opgoal.seq')
        stgoal_no = self.env['assessment.stgoal']. \
            browse(vals['relatedStrategicGoal']).seq
        vals['seq'] = stgoal_no + opgoal_no
        return super(OperationalGoal, self).create(vals)

    @api.multi
    def compute_count_projects(self):
        for rec in self:
            rec.project_count = self.env['project.project'].search_count([('relatedOperationalGoal', '=', rec.id)])
            
    def compute_count_comments(self):
        for rec in self:
            rec.comment_count = self.env['assessment.opgoalcomment'].search_count([('operationalGoal', '=', rec.id)])

    def compute_count_indicator(self):
        for rec in self:
            rec.indicator_count = self.env['assessment.indicator'].search_count([('operationalGoal', '=', rec.id)])

    @api.onchange('relatedStrategicGoal')
    def get_dep(self):
        self.operationalGoalDepartment = self.relatedStrategicGoal.strategicGoalDepartment

    @api.onchange('operationalGoalDepartment')
    def get_manager(self):
        self.operationalGoalResponsibleEmployee = self.operationalGoalDepartment.manager_id

    @api.depends('indicator_ids.progress', 'projects.progress')
    def _opgoal_progress_get(self):
        for record in self.sorted(key='id', reverse=True):
            if record.indicator_count != 0 or record.project_count != 0:
                for rec in record.indicator_ids:
                    record.somme += rec.progress
                for rec in record.projects:
                    record.somme += rec.progress
                general_count = record.indicator_count + record.project_count
                record.progress = record.somme / general_count
            else:
                record.progress = 0.0
