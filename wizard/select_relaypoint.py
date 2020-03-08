# -*- coding: utf-8 -*-
# This file is part of an Adiczion's Module.
# The COPYRIGHT and LICENSE files at the top level of this repository
# contains the full copyright notices and license terms.
from odoo import api, models, fields, _
import logging

_logger = logging.getLogger(__name__)


class RelayPointLine(models.TransientModel):
    _name = 'delivery.carrier.relaypoint.line'
    _description = 'Delivery Relay Point Line'
    
    name = fields.Char(index=True)
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    country_id = fields.Many2one(
        'res.country', string='Country', ondelete='restrict')
    code_relaypoint = fields.Char()
    hours = fields.Text(string='Hours', help='Office hours.')
    relay_id = fields.Many2one(
        'delivery.carrier.relaypoint', string='Relay Point')
    
    @api.multi
    def set_destination(self):
        context = dict(self.env.context or {})
        partner = self.relay_id.address.parent_id or self.relay_id.address
        # Build the delivery address ...
        addr = {
            'parent_id': partner.id,
            'type': 'delivery',
            'name': self.name,
            'street': self.street,
            'street2': self.street2,
            'zip': self.zip,
            'city': self.city,
            'code_relaypoint': self.code_relaypoint,
            'country_id': self.country_id and self.country_id.id
            }
        picking_id = self.env.context.get('picking_id')
        if picking_id:
            address = self.env['res.partner'].create(addr)
            # Set the delivery address to the picking
            picking = self.env['stock.picking'].browse(picking_id)
            picking.write({'partner_id': address.id})


class SelectRelayPoint(models.TransientModel):
    """Retrive relay point from reference address"""
    _name = 'delivery.carrier.relaypoint'
    _description = 'Delivery Relay Point'

    address = fields.Many2one(
        'res.partner', string='Reference address',
        help="We will look for the relay points around this address.")
    lines = fields.One2many(
        'delivery.carrier.relaypoint.line', 'relay_id', string='Lines',
        help="List of relay points found around the reference address.")

    def get_relaypoint(self):
        picking = self.env['stock.picking'].browse(
            self.env.context['picking_id'])
        relaypoints = picking.carrier_id.select_relaypoint([picking])
        points = []
        for point in relaypoints:
            value = dict(point.get('address'))
            value.update({'hours': '\n'.join([
                    _("{v[0]}: {v[1]}").format(v=val)
                    for val in point.get('hours')
                    ])})
            points.append([0, 0, value])
        if points:
            self.write({'lines' : points})
        context = dict(self.env.context or {})
        return {
            'name': _('Select the address'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'delivery.carrier.relaypoint',
            'view_id': self.env.ref(
                'a4o_delivery_relaypoint.select_relaypoint_view_form').id,
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'context': context,
            'target': 'new'
        }
