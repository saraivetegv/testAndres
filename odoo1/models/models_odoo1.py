from odoo import api, fields, models
from odoo.exceptions import UserError
import base64

class cuentaspredial(models.Model):
    _name="model.cuentaspredial"
    
    cuenta = fields.Char(String="Cuenta")
    contribuyente = fields.Char(String="Contribuyente")
    state = fields.Selection([('Abierto','Abierto'),('Pendiente','Pendiente'),('Cerrado','Cerrado')],String='Estado'
    ,readonly=True ,default="Abierto")
    #para buscar un numero en particular 
   # @api.multi
   # @api.constrains('cuenta')
   # def _check_cuentas(self):
    #    if self.cuenta in ('526'):
     #       raise UserError("Ya existe la cuenta")
            
        #para que no permite guardar el mismo valor
    @api.multi
    @api.constrains('cuenta')
    def _check_cuentas(self):
        for x in self:
            if x:
                if x.cuenta:
                    res = self.search([('cuenta','=',x.cuenta),('id','!=',x.id)])
                    if res:
                        raise UserError("Ya existe la cuenta")
                    
    #instanciar otro modelo y hacer una busqueda 
    @api.onchange('contribuyente')
    def _onchange_contribuyente(self):
        nombres = ""
        for x in self:
            if x.contribuyente:
                cont_obj = self.env['res.partner']
                contribuyente_ids = cont_obj.search([('name','like',x.contribuyente)])
                for i in contribuyente_ids:
                    nombres = i.name +" "+ nombres
               # raise UserError(nombres)
             
    #metodo para boton
    @api.multi
    def botond(self):
        variable1 = []
        variable2 = {}
        name = ""
        res = ""
        variable3 = self.env['res.partner']
        variable4 = variable3.search([('name','=',self.contribuyente)])
        if not variable4:
                    #name = i.name + name
                    variable2 = {
                            'name':self.contribuyente,
                    }
                    res = variable3.create(variable2)
                    variable1.append(variable2)
                    
        else:
            raise UserError("COntribuyente existente")
        return self.write({'state':'Pendiente'})
            
    #crear detalle y cabecera 
    @api.multi
    def botonpedidos(self):
        variable1 = []
        variable2 = {}
        name = ""
        res = ""
        variable3 = self.env['sale.order']
        variable5 = self.env['res.partner']
        variable4 = variable5.search([('name','=',self.contribuyente)])
        for x in variable4:
                    variable2 = {
                            'partner_id':x.id,
                    }
                    res = variable3.create(variable2)
                    variable1.append(variable2)
        i = 0
        producto =  self.env['sale.order.line']
        variable6 = {}
        variable7=[]
        var = ""
        while  i<5:
            variable6 = {
                           'order_id': res.id,
                           'product_id': 1
                    }
            var = producto.create(variable6)
            variable7.append(variable6)
            i+=1
          #sobreescribir          
        for r in var:
            r.write({'price_unit':23})
        return self.write({'state':'Cerrado'})
            
    @api.multi
    def reportprint(self):
        report = self.env['ir.attachment']
        report2 = "Predios"
        datos = base64.encodestring(report2)
        attach = {'name':'Reporte predios',
                  'datas':datos,
                  'datas_fname':'cuentas',
                  'description':'Reporte cuentas predial',
                  'res_model':'model.cuentaspredial',
                  'res_id':self.id,
                  'type':'binary'
        }
        report3 = report.create(attach)
        #raise UserError('Validar')
        return True
            
   