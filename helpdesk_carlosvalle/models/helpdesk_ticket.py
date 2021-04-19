from odoo import fields, models 

class HelpdeskTicket(models.Model):
    # nombre de la tabla en la bbdd
    _name = 'helpdesk.ticket'
    _description = 'Ticket'

    # string es para el nombre de la vista en odoo.
    # El nombre de la variable es para bbdd
    name = fields.Char(
        string= 'Name',required=True)
    description = fields.Text(
        string= 'Description',
        translate=True)
    date = fields.Date(
        string= 'Date'
    )

    state = fields.Selection(
        [('nuevo','Nuevo'),
         ('asignado','Asignado'),
         ('proceso','En proceso'),
         ('pendiente','Pendiente'),
         ('resuelto','Resuelto'),
         ('cancelado','Cancelado')],
        string='State',
        default='nuevo')

    time = fields.Float(
        string='Time')

    assigned = fields.Boolean(
        string='Assigned',
        readonly=True)

    date_limit = fields.Date(
        string='Date Limit')

    action_corrective = fields.Html(
        string='Corrective Action',
        help='Descrive corrective actions to do')
    
    action_preventive = fields.Html(
        string='Preventive Action',
        help='Descrive preventive actions to do')

    
    def asignar(self):
        self.write({'state':'asignado'
        , 'assigned': True })               # write me vale para escribir a la vez varios campos y leer varios registros quitando de ese modo for

        # for ticket in self:                 # self son varios registros, por lo que tenemos que hacerlo uno a uno en un for o con un write
        #     ticket.state = 'asignado'
        #     ticket.assigne = True           # mi objeto ticket lo estoy asignando


    def proceso(self):
        self.ensure_one()
        self.state = 'proceso'
    
    def pendiente(self):
        self.ensure_one()
        self.state = 'pendiente'

    def finalizar(self):
        self.ensure_one()
        self.state = 'resuelto'

    def cancelar(self):
        self.ensure_one()
        self.state = 'cancelado'
        