# -*- coding: utf-8 -*-
##############################################################################
#
#    Stock Inventory Valuation Related module for Odoo
#    Copyright (C) 2015 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class StockInventoryLine(models.Model):
    _inherit = 'stock.inventory.line'

    @api.one
    @api.depends('standard_price', 'product_qty')
    def compute_valuation(self):
        # We suppose that the UoM is not changed by the user in the inventory
        # line
        self.valuation = self.standard_price * self.product_qty

    standard_price = fields.Float(
        string='Cost Price',
        digits=dp.get_precision('Product Price'))
    valuation = fields.Float(
        compute='compute_valuation', digits=dp.get_precision('Account'),
        readonly=True, string='Valuation', store=True)

    @api.multi
    def onchange_createline(
            self, location_id, product_id, product_uom_id, package_id,
            prod_lot_id, partner_id):
        vals = super(StockInventoryLine, self).onchange_createline(
            location_id, product_id, product_uom_id, package_id,
            prod_lot_id, partner_id)
        if 'value' in vals and product_id:
            product = self.env['product.product'].browse(product_id)
            vals['value']['standard_price'] = product.standard_price
        return vals

    @api.model
    def create(self, vals):
        if vals.get('product_id') and not vals.get('standard_price'):
            product = self.env['product.product'].browse(vals['product_id'])
            vals['standard_price'] = product.standard_price
        return super(StockInventoryLine, self).create(vals)


class StockInventory(models.Model):
    _inherit = 'stock.inventory'

    @api.one
    @api.depends('line_ids.valuation')
    def compute_valuation(self):
        value = 0.0
        for line in self.line_ids:
            value += line.valuation
        self.valuation = value

    company_currency_id = fields.Many2one(
        related='company_id.currency_id', readonly=True)
    valuation = fields.Float(
        compute='compute_valuation', digits=dp.get_precision('Account'),
        readonly=True, string='Valuation')
