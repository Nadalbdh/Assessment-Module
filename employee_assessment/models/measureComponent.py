# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Measure(models.Model):
    _name = 'assessment.measure'

    name = fields.Char("Measure Component's Name")
    active = fields.Boolean('Active', default=True, required=True)
    indicator_id = fields.Many2one('assessment.indicator')
    year = fields.Many2one('date.range', string='Year')
    quarters = fields.One2many('assessment.period', 'measure', string='Quarters')
    quarters_count = fields.Integer(compute='compute_count_quarters')
    move = fields.Many2one('account.move', string='move')
    progress = fields.Float(compute='_progress_get', string='Progress', group_operator="avg", store=True)
    attachment_ids = fields.Many2many('ir.attachment', domain=[('res_model', '=', 'assessment.measure')],  string='Attachments')
    attachment_number = fields.Integer(compute='_get_attachment_number')

    @api.multi
    def compute_count_quarters(self):
        for rec in self:
            rec.quarters_count = self.env['assessment.period'].search_count([('measure', '=', rec.id)])

    @api.multi
    def action_get_attachment_tree_view(self):
        attachment_action = self.env.ref('base.action_attachment')
        action = attachment_action.read()[0]
        action['context'] = {'default_res_model': self._name, 'default_res_id': self.ids[0]}
        action['domain'] = str(['&', ('res_model', '=', self._name), ('res_id', 'in', self.ids)])
        return action

    @api.multi
    def _get_attachment_number(self):
        read_group_res = self.env['ir.attachment'].read_group(
            [('res_model', '=', 'assessment.measure'), ('res_id', 'in', self.ids)],
            ['res_id'], ['res_id'])
        attach_data = dict((res['res_id'], res['res_id_count']) for res in read_group_res)
        for record in self:
            record.attachment_number = attach_data.get(record.id, 0)

    @api.multi
    def get_year(self):
        self.year = self.env['date.range'].search([('type_id.fiscal_year', '=', True)])

    @api.depends('quarters.progress', 'quarters.type_id', 'quarters.type_id.fiscal_year')
    def _progress_get(self):
        for record in self:
            somme = 0.0
            if record.quarters_count != 0:
                for rec in record.quarters:
                    if rec.type_id.fiscal_year is True:
                        record.progress = rec.progress


class Period(models.Model):
    _name = 'assessment.period'

    name = fields.Char()
    range = fields.Many2one('date.range')
    date_end = fields.Date(related='range.date_end')
    parent_id = fields.Many2one('date.range', related='range.parent_id')
    type_id = fields.Many2one('date.range.type', related='range.type_id')
    past_range = fields.Boolean()
    expected_value = fields.Float('Expected Value')
    value_real = fields.Float('Real Value')
    measure = fields.Many2one('assessment.measure')
    progress = fields.Float(compute='_progress_get', store=True)

    @api.depends('expected_value', 'value_real')
    def _progress_get(self):
        for record in self:
            if record.expected_value != 0.0:
                record.progress = (100.0 * record.value_real / record.expected_value)
            else:
                record.progress = 0.0