from odoo import models, fields, api
from odoo.exceptions import ValidationError


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"

    name = fields.Char(required=True)

    @api.constrains('name')
    def _check_name_tag(self):
        for rec in self:
            if rec.name:
                raise ValidationError('Name Tag must be unique')
