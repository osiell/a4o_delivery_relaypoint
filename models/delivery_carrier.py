# -*- coding: utf-8 -*-
# This file is part of an Adiczion's Module.
# The COPYRIGHT and LICENSE files at the top level of this repository
# contains the full copyright notices and license terms.
from odoo import api, models, fields, _
import logging

_logger = logging.getLogger(__name__)


#class DeliveryRelayPoint(models.Model):
#    _name = 'delivery.carrier.relaypoint'
#    _description = "Relay Point for Delivery"

#    name = fields.Boolean('Name', required=True)
#    access_reduced_mobility = fields.Boolean(
#        string="Access Reduced Mobility",
#        help="Access for people with reduced mobility")


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'
    
    def select_relaypoint(self, pickings):
        ''' [TODO] Update this description ....
        Send the package to the service provider

        :param pickings: A recordset of pickings
        :return list: A list of dictionaries (one per picking) containing of the form::
                         { 'exact_price': price,
                           'tracking_number': number }
                           # TODO missing labels per package
                           # TODO missing currency
                           # TODO missing success, error, warnings
        '''
        self.ensure_one()
        _logger.debug('select_relaypoint: %s' % pickings)
        if hasattr(self, '%s_select_relaypoint' % self.delivery_type):
            return getattr(
                self, '%s_select_relaypoint' % self.delivery_type)(pickings)
