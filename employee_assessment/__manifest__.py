# -*- coding: utf-8 -*-
{
    'name': "Assessment",

    'summary': """
        Assessment Platform""",

    'description': """
       
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/10.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'hr',
                'document',
                'project',
                'hr_timesheet',
                'board',
                ],

    # always loaded
    'data': [
        'security/security_group.xml',
        'security/ir.model.access.csv',
        'views/assessment_template.xml',
        'views/projects.xml',
        'views/award.xml',
        'views/strategicGoal.xml',
        'views/operationalGoal.xml',
        'views/comment.xml',
        'views/indicator.xml',
        'views/projects.xml',
        'views/assessor_views.xml',
        'views/attachment.xml',
        'views/component.xml',
        'views/timePeriods.xml',
        'views/dashboard.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'application': 'True',
}