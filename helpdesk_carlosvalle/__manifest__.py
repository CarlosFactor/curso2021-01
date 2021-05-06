{
    'name': "Helpdesk_Carlos_Valle",

    'summary': """ Carlos Helpdesk""",

    'description': """ Helpdesk""",

    'author': "Carlos del Valle",
    'website': "http://www.factorlibre.com",

    'category': 'Uncategorized',
    'version': '14.0.1.0.0',

    'depends': [
        'base',
        'mail'],

    'license': 'AGPL-3',
    
    'data':[
        'security/helpdesk_security.xml',
        'security/ir.model.access.csv',
        "reports/helpdesk_ticket_report_templates.xml",
        "reports/res_partner_templates.xml",
        'views/helpdesk_menu.xml',
        'views/helpdesk_view.xml',
        'wizards/create_ticket_view.xml',
        'views/helpdesk_tag_view.xml',
        #'data/delete_tag_cron.xml',
    ]
}