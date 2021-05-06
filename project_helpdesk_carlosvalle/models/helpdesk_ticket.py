from odoo import models, fields, api, _


class HelpdeskTicket(models.Model):
    _name = 'helpdesk.ticket'   # Me creo un nuevo modelo.
    _description = 'Ticket'
    # Este nuevo modelo hereda de project.task
    _inherits = {'project.task': 'task_id'} # Heredamos del project.task

    @api.model
    def default_get(self, fields):
        defaults = super(HelpdeskTicket, self).default_get(fields)
        # Actualizamos el campo project_id y que sera igual 
        defaults.update({
            # self.env.ref toma una cadena con un ID externo y devuelve un registro
            # Como yo me estoy creando un proyecto con un identificador lo indicaremos, dicho identificador pertenece al data
            # Antes de ese identificador le pondremos el nombre del modulo
            # Le ponemos .id para que me devuelva el identificador
            'project_id': self.env.ref('project_helpdesk_carlosvalle.project_helpdkesk').id
        })
        return defaults

    # Creamos el campo task_id que apuntara a los campos que yo quiera.
    task_id = fields.Many2one(
        comodel_name='project.task', # Va a apuntar al project.task
        string='Task',
        auto_join=True, index=True, ondelete="cascade", required=True)

    action_corrective = fields.Html(
        string='Corrective Action',
        help='Descrive corrective actions to do')

    action_preventive = fields.Html(
        string='Preventive Action',
        help='Descrive preventive actions to do')
    
    def action_assign_to_me(self):
        self.ensure_one()
        return self.task_id.action_assign_to_me()
    
    # Al ser de tipo object podemos realizar el metodo
    def action_subtask(self):
        self.ensure_one()
        return self.task_id.action_subtask()
    
    def action_recurring_tasks(self):
        self.ensure_one()
        return self.task_id.action_recurring_tasks()

    def _message_get_suggested_recipients(self):
        self.ensure_one()
        return self.task_id._message_get_suggested_recipients()