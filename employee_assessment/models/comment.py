# -*- coding: utf-8 -*-


from odoo import api, fields, models


class awardComment(models.Model):
    _name = 'assessment.awardcomment'

    name = fields.Char('comment name')
    comment_body = fields.Text('comment body')
    comment_date = fields.Datetime(default=fields.Datetime.now, readonly=True)
    award = fields.Many2one('assessment.award', string="award")
    done = fields.Boolean('Done')


class StGoalComment(models.Model):
    _name = 'assessment.stgoalcomment'
    _inherit = 'assessment.awardcomment'

    strategicGoal = fields.Many2one('assessment.stgoal', string="Strategic Goal")


class OpGoalComment(models.Model):
    _name = 'assessment.opgoalcomment'
    _inherit = 'assessment.awardcomment'

    operationalGoal = fields.Many2one('assessment.opgoal', string="Operational goal")


class ProjectComment(models.Model):
    _name = 'assessment.projectcomment'
    _inherit = 'assessment.awardcomment'

    project = fields.Many2one('project.project', string="Project")


class TaskComment(models.Model):
    _name = 'assessment.taskcomment'
    _inherit = 'assessment.awardcomment'

    relatedTask = fields.Many2one('project.task', string="Task")


class IndicatorComment(models.Model):
    _name = 'assessment.indicatorcomment'
    _inherit = 'assessment.awardcomment'

    indicator = fields.Many2one('assessment.indicatorcomment', string="indicator")
