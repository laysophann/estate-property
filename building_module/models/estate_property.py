from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = 'Real Estate Properties'
    _order = "id desc"


    name = fields.Char(required=True, string="Title")
    description = fields.Text()
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(default=lambda self: datetime.today() + timedelta(days=90), string="Available From")
    expected_price = fields.Float(required=True, string="Expected Price")
    selling_price = fields.Float(readonly=True, string="Selling Price")
    bedrooms = fields.Integer(default=2, string="Bedrooms")
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [('north', 'North'),
         ('south', 'South'),
         ('east', 'East'),
         ('west', 'West')]
    )
    state = fields.Selection(
        [('new', 'New'),
         ('offer_received', 'Offer Received'),
         ('offer_accepted', 'Offer Accepted'),
         ('sold', 'Sold'),
         ('cancel', 'Canceled')], required=True, readOnly=True, default='new'
    )
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    seller_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string="Buyer")
    property_tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    total_area = fields.Integer(string="Total Area (sqm)", compute='_compute_total_area')
    best_price = fields.Integer(string="Best Offer", compute='_compute_best_price', inverse='_inverse_best_price')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for rec in self:
            rec.best_price = rec.offer_ids and max(rec.offer_ids.mapped('price')) or 0

    def _inverse_best_price(self):
        for rec in self:
            best_offer = rec.offer_ids.filtered(lambda offer: offer.price == rec.best_price)
            if best_offer:
                rec.buyer_id = best_offer.partner_id

    @api.onchange("garden")
    def _onchange_garden(self):
        if not self.garden:
            self.garden_area = 0
            self.garden_orientation = False
        else:
            self.garden_area = 10
            self.garden_orientation = 'north'

    def action_cancel_button(self):
        for rec in self:
            if rec.state == 'sold':
                raise UserError(_("Sold property can't be Canceled."))
            rec.state = 'cancel'
        return True

    def action_sold_button(self):
        for rec in self:
            if rec.state == 'cancel':
                raise UserError(_("Canceled property can't be sold."))
            rec.state = 'sold'
        return True

    @api.constrains('expected_price', 'best_price', 'selling_price')
    def _check_expected_price(self):
        for rec in self:
            percentage = (rec.best_price / rec.expected_price * 100)
            if rec.expected_price < 0:
                raise ValidationError(_("The expected price must be strictly positive."))
            if rec.best_price < 0:
                raise ValidationError(_("The offer price must be strictly positive."))
            if percentage < 90:
                raise ValidationError(_("The selling price must be at least 90% of the expected price."))
