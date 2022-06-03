# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models
from odoo import tools, _
from odoo.modules.module import get_module_resource


_logger = logging.getLogger(__name__)


class Assessor(models.Model):
    _name = 'assessment.assessor'
    _inherit = 'hr.employee'
    _description = 'assessor profile and CV'
    _order = 'name_related'
    _inherits = {'resource.resource': "resource_id"}
    _inherit = ['mail.thread']

    _mail_post_access = 'read'

    @api.model
    def _default_image(self):
        image_path = get_module_resource('hr', 'static/src/img', 'default_image.png')
        return tools.image_resize_image_big(open(image_path, 'rb').read().encode('base64'))

    name_related = fields.Char(related='resource_id.name', string="Resource Name", readonly=True, store=True)
    country_id = fields.Many2one('res.country', string='Nationality (Country)')
    birthday = fields.Date('Date of Birth', groups='hr.group_hr_user')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], groups='hr.group_hr_user')
    marital = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('widower', 'Widower'),
        ('divorced', 'Divorced')
    ], string='Marital Status', groups='hr.group_hr_user')
    address_id = fields.Many2one('res.partner', string='Working Address')
    address_home_id = fields.Many2one('res.partner', string='Home Address')
    work_phone = fields.Char('Work Phone')
    mobile_phone = fields.Char(string='Work Mobile', required=True)
    work_email = fields.Char(string='Work Email', required=True)
    work_location = fields.Char('Work Location')
    notes = fields.Text('Notes')
    child_ids = fields.One2many('hr.employee', 'parent_id', string='Subordinates')
    resource_id = fields.Many2one('resource.resource', string='Resource',
                                  ondelete='cascade', required=True, auto_join=True)
    color = fields.Integer('Kanban Color Indicator', default=0)
    city = fields.Char(related='address_id.city')
    login = fields.Char(related='user_id.login', readonly=True)
    last_login = fields.Datetime(related='user_id.login_date', string='Latest Connection', readonly=True)

    # image: all image fields are base64 encoded and PIL-supported
    image = fields.Binary("Photo", default=_default_image, attachment=True,
                          help="This field holds the image used as photo for the employee, limited to 1024x1024px.")
    image_medium = fields.Binary("Medium-sized photo", attachment=True,
                                 help="Medium-sized photo of the employee. It is automatically "
                                      "resized as a 128x128px image, with aspect ratio preserved. "
                                      "Use this field in form views or some kanban views.")
    image_small = fields.Binary("Small-sized photo", attachment=True,
                                help="Small-sized photo of the employee. It is automatically "
                                     "resized as a 64x64px image, with aspect ratio preserved. "
                                     "Use this field anywhere a small image is required.")

    past_experience = fields.One2many('assessment.experience', 'related_assessor',
                                      string="Past Experience")
    attachment_ids = fields.One2many('ir.attachment', 'res_id', domain=[('res_model', '=', 'assessment.assessor')], string='Attachments')
    interest_domains = fields.One2many('assessment.interest', 'related_assessor',
                                       string="Domains of Interest", required=True )

    @api.multi
    def action_get_attachment_tree_view(self):
        attachment_action = self.env.ref('base.action_attachment')
        action = attachment_action.read()[0]
        action['context'] = {'default_res_model': self._name, 'default_res_id': self.ids[0]}
        action['domain'] = str(['&', ('res_model', '=', self._name), ('res_id', 'in', self.ids)])
        return action


class InterestDomain(models.Model):
    _name = 'assessment.interest'

    name = fields.Char('Domain of Interest', required=True)
    related_assessor = fields.Many2one('assessment.assessor', string="related_assessor")


class Experience(models.Model):
    _name = 'assessment.experience'

    name = fields.Char('Place of Work')
    experience_start = fields.Date('From')
    experience_end = fields.Date('To')
    related_assessor = fields.Many2one('assessment.assessor', string="related_assessor")

