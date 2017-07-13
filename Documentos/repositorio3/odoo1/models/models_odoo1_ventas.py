from odoo import api, fields, models
from odoo.exceptions import UserError

class ventasclientes(models.Model):
    _inherit = "res.partner"
    
    facebook = fields.Char(String="Facebook")
