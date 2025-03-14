from datetime import timedelta
from odoo import models, fields, api


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
        [
            ('refused', 'Refused'),
            ('accepted', 'Accepted')], copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(string="Validity (day)s", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline",
                                tracking=True)

    @api.depends("validity", "property_id.date_availability")
    def _compute_deadline(self):
        for rec in self:
            if rec.validity:
                rec.date_deadline = fields.Date.today() + timedelta(days=rec.validity)
            else:
                rec.date_deadline = False

    def _inverse_deadline(self):
        for rec in self:
            if rec.date_deadline:
                rec.validity = (rec.date_deadline - fields.Date.today()).days
            else:
                rec.validity = 0

    def action_button_accept(self):
        print('action_button_accept')
        for rec in self:
            rec.status = 'accepted'
            rec.property_id.selling_price = rec.price
            rec.property_id.buyer_id = rec.partner_id

    def action_button_refuse(self):
        print('action_button_refuse')
        for rec in self:
            rec.status = 'refused'
            rec.property_id.selling_price = 0
            rec.property_id.buyer_id = False
