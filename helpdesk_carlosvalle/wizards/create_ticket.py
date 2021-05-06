from odoo import models, api, fields, _


class CreateTicket(models.TransientModel):
    _name = 'create.ticket'

    name = fields.Char()

    def create_ticket(self):
        self.ensure_one()
        # Compruebo que lo estoy lanzando desde una etiqueta
        active_id = self._context.get('active_id', False)
        if active_id and self._context.get('active_model') == 'helpdesk.ticket.tag':
            # Creamos un ticket 
            ticket = self.env['helpdesk.ticket'].create({
                'name': self.name,
                'tag_ids': [(6, 0, [active_id])]
            })
            # Abrimos el ticket utilizando una accion que ya he creado 
            action = self.env.ref('helpdesk_carlosvalle.helpdesk_ticket_action').read()[0]
            # Con esto le decimos que me abra justo el que yo he creado 
            action['res_id'] = ticket.id
            # Le decimos que esta accion me la abra en tipo formulario      
            action['views'] = [(self.env.ref('helpdesk_carlosvalle.view_helpdesk_ticket_form').id,'form')]
            return action
        return {'type': 'ir.actions.act_window_close'}