from odoo import fields, models, api, _ 
from odoo.exceptions import ValidationError
from datetime import timedelta

class HelpdeskTicketAction(models.Model):
    _name = 'helpdesk.ticket.action'
    _description = 'Action'

    name = fields.Char()                    # Campo name
    date = fields.Date()                    # Campo date 
    time = fields.Float(
        string='Time')

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

    public = fields.Boolean()

    # Añadir un m2m en helpdeskticket.tag para ver todas las tareas relacionadas con cada tag
    # Esto nos sirver para saber qie tickets estan asociados a una etiqueta 
    tickets_ids = fields.Many2many(
        comodel_name='helpdesk.ticket',     # Ponemos el modelo del que queremos coger los datos
        relation='helpdesk_ticket_tag_rel', # Como quiero que se llame la tabla intermedia
        column1='tag_id',                   # Cual es la columna que apunta a mi tabla 
        column2='ticket_id',                # Cual es la columna que apunta a la otra tabla
        string='Tickets')

    # @api.model
    # def cron_delete_tag(self):
    #     tickets = self.search([('tickets_ids','=',False)])
    #     tickets.unlink()



class HelpdeskTicket(models.Model):
    # nombre de la tabla en la bbdd
    _name = 'helpdesk.ticket'
    _description = 'Ticket'

    _inherit = ['mail.thread.cc',
                'mail.thread.blacklist', 
                'mail.activity.mixin']

    _primary_email = 'email_from'



    # ----------------------- Funciones del default ---------------------------------------

    # Metodo para que nos devuelva la fecha de hoy en el Date
    def _date_default_today(self):
        return fields.Date.today()


    # Metodo para que nos devuelva la fecha de mañana en el Date
    # @api.Model
    # def default_get(self, default_fields):
    #     vals = super(HelpdeskTicket,self).default_get(default_fields)
    #     vals.update({'date': fields.Date.today() + timedelta(days=1)})
    #     return vals


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
        string='Time',
        compute='_get_time',
        inverse='_set_time',
        search='_search_time')

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

    # Creamos el campo partner que estara relaciona con res.partner
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner')

    email_from = fields.Char(
        string='Email from')

    # ----------------------- Metodos ------------------------------ 


    @api.depends('action_ids.time') # va a depender de que yo modifique los time para actualizarmelos 
    def _get_time(self):
        for record in self:
            record.time = sum(record.action_ids.mapped('time')) 


    #Este es el metodo del inverse 
    def _set_time(self):        
        for record in self:
            if record.time:
                time_now = sum(record.action_ids.mapped('time')) 
                next_time = record.time - time_now
                if next_time:
                    data = {
                        'name': '/', 'time': next_time, 
                        'date': fields.Date.today(), 
                        'ticket_id': record.id
                        }
                    self.env['helpdesk.ticket.action'].create(data)


    # Funcion que buscara tickes o acciones donde el tiempo sea mayor que el indicado 
    def _search_time(self, operator, value):
        actions = self.env['helpdesk.ticket.action'].search([('time',operator,value)])
        return [('id', 'in', actions.mapped('ticket_id').ids)]


    def asignar(self):
        self.ensure_one()           # Esto hace que solo se ejecute sobre un registro
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

    def cancelar_multi(self):
        for record in self:
            record.cancelar()


    @api.depends('user_id')  
    def _compute_assigned(self):
        for record in self:
            # Si user_id tiene algo sera verdadero y si no tiene nada sera falso
            record.assigned = self.user_id and True or False



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
        # self.write({
        #     'tag_ids': [(0,0, {'name':self.tag_name})]})

        # opcion 2 (la mas sencilla)
        # tag = self.env['helpdesk.ticket.tag'].create({
        #     'name': self.tag_name
        # })
        # self.write({
        #     'tag_ids': [(4,tag.id,0)]
        # })
        #self.tag_name = False


        # Modificar el botón de crear una etiqueta en el formulario de ticket para que abra una acción nueva,
        # pasando por contexto el valor del nombre y la relación con el ticket.

        action = self.env.ref('helpdesk_carlosvalle.action_new_tag').read()[0]

        action['context'] = {
            'default_name': self.tag_name,              # Con esto coge el nombre del campo que le pasamos nosotros y lo introduce en el form por defecto
            'default_tickets_ids': [(6,0,self.ids)]     # Coge los campos del ticket fecha y nombre del ticket y los introduce en el form 
        }
        # action['res_id'] = tag.id
        self.tag_name = False
        return action
        


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


    # Funcion para que al indicar la fecha y las horas, en base a las horas, 
    # nos ponga un da mas en la fecha limite
    @api.onchange( 'date','time')
    def _onchange_date (self):
        date_limit = self.date and self.date + timedelta(hours=self.time)
        self.date_limit = date_limit

    





