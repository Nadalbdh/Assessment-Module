# -*- coding: utf-8 -*-


from odoo import api, fields, models


class Risk(models.Model):
    _name = 'assessment.risk'

    name = fields.Char('Risk')
    description = fields.Text('Description')
    risk_degree = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], string='Degree of Risk')

    risk_potential = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], string='Potential of Risk')

    risk_priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], string='Priority Risk Treatment ')


class StGoalRisk(models.Model):
    _name = 'assessment.stgoalrisk'
    _inherit = 'assessment.risk'

    strategicGoal = fields.Many2one('assessment.stgoal', string="Strategic Goal")


class IndicatorRisk(models.Model):
    _name = 'assessment.indicatorrisk'
    _inherit = 'assessment.risk'

    indicator = fields.Many2one('assessment.indicator', string="indicator")


class OpGoalRisk(models.Model):
    _name = 'assessment.opgoalrisk'
    _inherit = 'assessment.risk'

    operationalGoal = fields.Many2one('assessment.opgoal')


class ProjectRisk(models.Model):
    _name = 'assessment.projectrisk'
    _inherit = 'assessment.risk'

    relatedProject = fields.Many2one('project.project')

