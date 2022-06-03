# -*- coding: utf-8 -*-
from odoo import http

# class EmployeeAssessment(http.Controller):
#     @http.route('/employee_assessment/employee_assessment/', auth='public')
#     def indicator(self, **kw):
#         return "Hello, world"

#     @http.route('/employee_assessment/employee_assessment/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('employee_assessment.listing', {
#             'root': '/employee_assessment/employee_assessment',
#             'objects': http.request.env['employee_assessment.employee_assessment'].search([]),
#         })

#     @http.route('/employee_assessment/employee_assessment/objects/<model("employee_assessment.employee_assessment"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('employee_assessment.object', {
#             'object': obj
#         })