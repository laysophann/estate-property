from odoo import models, fields, api
from odoo.exceptions import ValidationError


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence,name"

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")

    # @api.model
    # def create(self, vals):
    #     vals['sequence'] = self.env['ir.sequence'].next_by_code('estate.property.type')
    #     return super().create(vals)

    @api.constrains('name')
    def _check_name_type(self):
        for rec in self:
            if rec.search_count([('name', '=', rec.name)]) > 1:
                raise ValidationError(f"{rec.name} already exists.")
