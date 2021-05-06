from odoo import fields, models, api, _ 

class SaleOrder(models.Model):      # Creamos la clase en base al modelo sale.oder

    # Con esto estamos heredando del modelo sale.order del modulo Sales
    _inherit = 'sale.order'         

    # Añadimos un campo ticket_ids que estara relacionado con mi modelo helpdesk.ticket
    ticket_ids = fields.One2many(
        comodel_name='helpdesk.ticket',
        inverse_name='sale_id',
        string="Tickets")


    # Creamos una funcion para crear tickets
    def create_ticket(self):
        self.ensure_one()       # Lo voy a lanzar desde un pedido, pondre el boton en un pedido

        # Este tag_ids es mi pedido. Mapped se encarga de hacer el mapeo de todos los productos de todas mis lineas.
        # Con ids nos devuelve el listado de mis tags 
        tag_ids = self.order_line.mapped('product_id.helpdesk_tag_id').ids

        # Buscamos el objeto helpdesk.ticket y hacemos un create indicando los campos que queremos 
        self.env['helpdesk.ticket'].create({
            'name': '%s Issue'%(self.name),     # El %s va a esperar un string que sera el nombre del sale order 
            'tag_ids': [(6, 0, tag_ids)],       # Al ser Many2many con esto añade todos los ids a la relacion
            'sale_id': self.id                  
        })


    def action_cancel(self):
        self.ticket_ids.cancelar_multi()
        # Indicamos cual es el nombre de la clase 
        return super(SaleOrder,self).action_cancel()