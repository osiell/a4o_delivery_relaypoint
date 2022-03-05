# This file is part of an Adiczion's Module.
# The COPYRIGHT and LICENSE files at the top level of this repository
# contains the full copyright notices and license terms.
from odoo import api, models, fields, _
import logging

_logger = logging.getLogger(__name__)


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'
    
    @api.depends('delivery_type')
    def _compute_delivery_relaypoint(self):
        for record in self:
            delivery = record.delivery_type
            if hasattr(record, '%s_get_delivery_relaypoint' % delivery):
                record.relaypoint_delivery = getattr(record,
                    '%s_get_delivery_relaypoint' % delivery)()

    relaypoint_delivery = fields.Boolean('Delivery to a relay point ?',
        compute='_compute_delivery_relaypoint', store=False)

    @api.model
    def _print_document(self, label, printer):
        """ Print a label, do not return the document file """
        if not printer:
            log_message = (_("No direct printer defined! Please check the "
                    "configuration of your delivery method."))
            self.message_post(body=log_message)
            return False
        return printer.print_document(self, label,
            doc_format='pdf', action='server', tray='Main')

    def select_relaypoint(self, **data):
        """Call the method to select relay points of the selected carrier"""
        self.ensure_one()
        _logger.debug('select_relaypoint: %s' % data)
        if hasattr(self, '%s_select_relaypoint' % self.delivery_type):
            return getattr(
                self, '%s_select_relaypoint' % self.delivery_type)(**data)

    def add_address(self, partner_id, address):
        '''
        :param address: dict of address
        '''
        Partner = self.env['res.partner']
        parent_id = partner_id.parent_id or partner_id
        address.update({
            'parent_id': parent_id.id,
            'type': 'delivery',
            'point_type': address.get('point_type', None),
            'active': False if self.hide_partner else True,
            })
        address_id = Partner.search([
                ('parent_id', '=', parent_id.id),
                ('type', '=', 'delivery'),
                ('code_relaypoint', '=', address.get('code_relaypoint')),
                ('active', 'in', [True, False]),
                ])
        if not address_id:
            address_id = Partner.create(address)
        return address_id

