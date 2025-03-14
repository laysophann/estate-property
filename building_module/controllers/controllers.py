# -*- coding: utf-8 -*-
# from odoo import http


# class BuildingModule(http.Controller):
#     @http.route('/building_module/building_module', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/building_module/building_module/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('building_module.listing', {
#             'root': '/building_module/building_module',
#             'objects': http.request.env['building_module.building_module'].search([]),
#         })

#     @http.route('/building_module/building_module/objects/<model("building_module.building_module"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('building_module.object', {
#             'object': obj
#         })

