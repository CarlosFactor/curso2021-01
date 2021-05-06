from odoo import fields, models, api, _ 

class ProductProduct(models.Model):
    # Hereda del modelo product.product perteneciente a Products
    _inherit = 'product.product'

    # Le añadimos un campo etiqueta, como solo es una sera Many2one
    helpdesk_tag_id = fields.Many2one(
        comodel_name = 'helpdesk.ticket.tag',
        string = 'Helpdesk Tag')