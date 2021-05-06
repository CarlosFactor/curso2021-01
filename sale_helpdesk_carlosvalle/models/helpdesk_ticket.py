from odoo import fields, models, api, _ 

class HelpdeskTicket(models.Model):
    # Le indicamos de la clase que hereda 
    _inherit='helpdesk.ticket'

    # Este campo esta relacionado con ticket_ids de la clase sale.order
    sale_id = fields.Many2one(
        comodel_name='sale.order',
        string = 'Sale Order')