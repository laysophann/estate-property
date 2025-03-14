from odoo import models, fields, api
from odoo.exceptions import ValidationError


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    name = fields.Char(required=True)

    @api.constrains('name')
    def _check_name_type(self):
        for rec in self:
            if rec.name:
                raise ValidationError('Name Type must be unique')
