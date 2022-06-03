# -*- coding: utf-8 -*-


from odoo import api, fields, models


class Project(models.Model):
    _inherit = 'project.project'

    relatedOperationalGoal = fields.Many2one('assessment.opgoal', string="Operational Goal")
    comments = fields.One2many('assessment.projectcomment', 'project', string="Comments")
    dangers = fields.One2many('assessment.projectrisk', 'relatedProject')
    progress = fields.Float(compute='_project_progress_get', string='Progress', store=True)

    @api.depends('tasks.progress')
    def _project_progress_get(self):
        for record in self.sorted(key='id', reverse=True):
            somme = 0.0
            if record.task_count != 0:
                for rec in record.tasks:
                    somme += rec.progress
                record.progress = somme / record.task_count
            else:
                record.progress = 0.0


class Task(models.Model):
    _inherit = 'project.task'

    comments = fields.One2many('assessment.taskcomment', 'relatedTask', string="Comments")
    task_type = fields.Selection([
        ('regular', 'Regular'),
        ('enhancement', 'Enhancement')
    ], string='Task Type', default='regular')