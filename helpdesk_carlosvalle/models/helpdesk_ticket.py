from odoo import fields, models 

class HelpdeskTicket(models.Model):
    # nombre de la tabla en la bbdd
    _name = 'helpdesk.ticket'
    _description = 'Ticket'

    # string es para el nombre de la vista en odoo.
    # El nombre de la variable es para bbdd
    name = fields.Char(
        string = 'Name')
    description = fields.Text(
        string = 'Description')
    date = fields.Date(
        string = 'Date'
    )