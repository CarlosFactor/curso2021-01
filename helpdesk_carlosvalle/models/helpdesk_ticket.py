from odoo import fields, models, api, _ 
from odoo.exceptions import ValidationError
from datetime import timedelta

class HelpdeskTicketAction(models.Model):
    _name = 'helpdesk.ticket.action'
    _description = 'Action'

    name = fields.Char()                    # Campo name
    date = fields.Date()                    # Campo date 

    # Vamos a definir que una accion seria como la linea de un presupuesto de ventas.
    # Una accion solo puede estar en un ticket 
    # Este many2one apuntara a helpdeskticket.
    ticket_id = fields.Many2one(            
        comodel_name='helpdesk.ticket',
        string='Ticket')




class HelpdeskTicketTag(models.Model):
    _name = 'helpdesk.ticket.tag'
    _description = 'Tag'

    name = fields.Char()


    # Añadir un m2m en helpdeskticket.tag para ver todas las tareas relacionadas con cada tag
    # Esto nos sirver para saber qie tickets estan asociados a una etiqueta 
    tickets_ids = fields.Many2many(
        comodel_name='helpdesk.ticket',     # Ponemos el modelo del que queremos coger los datos
        relation='helpdesk_ticket_tag_rel', # Como quiero que se llame la tabla intermedia
        column1='tag_id',                   # Cual es la columna que apunta a mi tabla 
        column2='ticket_id',                # Cual es la columna que apunta a la otra tabla
        string='Tickets')




class HelpdeskTicket(models.Model):
    # nombre de la tabla en la bbdd
    _name = 'helpdesk.ticket'
    _description = 'Ticket'




    # ----------------------- Funciones del default ---------------------------------------

    # Metodo para que nos devuelva la fecha de hoy en el Date
    def _date_default_today(self):
        return fields.Date.today()



    # string es para el nombre de la vista en odoo.
    # El nombre de la variable es para bbdd
    name = fields.Char(
        string= 'Name',required=True)

    description = fields.Text(
        string= 'Description',
        translate=True)

    date = fields.Date(
        string= 'Date',
        default= _date_default_today)

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
        compute='_compute_assigned')

    date_limit = fields.Date(
        string='Date Limit')

    action_corrective = fields.Html(
        string='Corrective Action',
        help='Descrive corrective actions to do')
    
    action_preventive = fields.Html(
        string='Preventive Action',
        help='Descrive preventive actions to do')


    # Esto indica que dentro de mi ticket asocio un usuario, un usuario puede estar asociado a muchos tickets
    user_id = fields.Many2one(      # Habra una columna que sea user id y apunte al otro id 
        comodel_name='res.users',   #
        string='Assigned to'        # A quien esta asignando el ticjet 
    )

    tag_ids = fields.Many2many(
        comodel_name='helpdesk.ticket.tag', # Ponemos el modelo aqui 
        relation='helpdesk_ticket_tag_rel', # Como quiero que se llame la tabla intermedia
        column1='ticket_id',                # Le indicamos cual es la columna que apunta a mi tabla 
        column2='tag_id',                   # Cual es la clumna que apunta a la otra tabla 
        string='Tags')                      # Nombre que le damos 

    # Esto apuntan al ticket 
    action_ids = fields.One2many(               
        comodel_name='helpdesk.ticket.action',  # Esto apunta a este modelo 
        inverse_name='ticket_id',               # Cual es el campo del modelo anterior que apunta al mio 
        string='Actions')                       # Como se va a llamar 


    # Declaramos color de tipo entero diciendole que es un campo calculado del metodo color_estado
    color= fields.Integer('Color Index',default=10, compute='color_estado')





    # ----------------------- Metodos ------------------------------ 



    
    def asignar(self):
        self.ensure_one()
        self.write({
            'state':'asignado',      # write me vale para escribir a la vez varios campos y leer varios registros quitando de ese modo for
            'assigned': True })               # Le pasaremos un diccionario indicando que cosas quiero escribir

        # En caso de ser un solo campo podriamos hacerlo del siguiente modo 
        # for ticket in self:                 
        #     ticket.state = 'asignado'
        #     ticket.assigne = True           

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


    @api.depends('user_id')  
    def _compute_assigned(self):
        for record in self:
            record.assigned = self.user_id and True or False # Si user_id tiene algo sera verdadero y si no tiene nada sera falso
    


    # Hacer un campo calculado que indique, dentro de un ticket
    # la cantidad de tickets asociados al mismo usuario 
    ticket_qty = fields.Integer(
        string='Ticket Qty',            # Le paso el string
        compute='_compute_ticket_qty')  # Con esto le estoy pasando el nombre del metodo

    
    @api.depends('user_id')
    def _compute_ticket_qty(self):
        for record in self:         
            other_tickets = self.env['helpdesk.ticket'].search([('user_id', '=', record.user_id.id)])
            record.ticket_qty = len(other_tickets)


    # Crear un campo nombre de etiqueta y hacer un boton que cree la nueva etiqueta con ese nombre y lo asocie al ticket
    tag_name = fields.Char(
        string='Tag_Name')

    def create_tag(self):
        self.ensure_one()       # V a ser un boton que va a estar dentro de mi formulario
        # opcion 1 (mas optima)
        self.write({
            'tag_ids': [(0,0, {'name':self.tag_name})]})

        # opcion 2 (la mas sencilla)
        # tag = self.env['helpdesk.ticket.tag'].create({
        #     'name': self.tag_name
        # })
        # self.write({
        #     'tag_ids': [(4,tag.id,0)]
        # })
        self.tag_name = False

        
    # Con este metodo cambiamos el color de las tarjetas en la vista kanban en base al estado del cliente 
    @api.depends('state')
    def color_estado(self):
        for record in self:
            diccionario_colores_dict={
                'nuevo': 1,
                'asignado': 2,
                'en_proceso': 3,
                'pendiente': 4,
                'resuelto': 5,
                'cancelado': 6
            }
            record.color = diccionario_colores_dict[record.state]
    


    @api.constrains( 'time')
    def _time_positive (self):
        for ticket in self:
            if ticket.time and ticket.time < 0:
                raise ValidationError (_("The time can not be negative" ))



    @api.onchange( 'date','time')
    def _onchange_date (self):
        date_limit = self.date and self.date + timedelta(hours=self.time)
        self.date_limit = date_limit

    