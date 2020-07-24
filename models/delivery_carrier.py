# This file is part of an Adiczion's Module.
# The COPYRIGHT and LICENSE files at the top level of this repository
# contains the full copyright notices and license terms.
from odoo import api, models, fields, _
import logging

_logger = logging.getLogger(__name__)


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    def select_relaypoint(self, pickings):
        """Call the method to select relay points of the selected carrier"""
        self.ensure_one()
        _logger.debug('select_relaypoint: %s' % pickings)
        if hasattr(self, '%s_select_relaypoint' % self.delivery_type):
            return getattr(
                self, '%s_select_relaypoint' % self.delivery_type)(pickings)
