# -*- coding: utf-8 -*-
# © 2013 - Today: GRAP (http://www.grap.coop)
# © 2015-2018 Akretion (http://www.akretion.com)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class StockInventoryLine(models.Model):
    _inherit = 'stock.inventory.line'

    @api.depends(
        'standard_price', 'product_qty', 'product_uom_id', 'product_id')
    def _compute_valuation(self):
        for line in self:
            if line.product_uom_id and line.product_id:
                qty_product_uom = line.product_uom_id._compute_quantity(
                    line.product_qty, line.product_id.uom_id)
            else:
                qty_product_uom = line.product_qty
            line.valuation = line.standard_price * qty_product_uom

    standard_price = fields.Float(
        string='Cost Price',
        digits=dp.get_precision('Product Price'),
        help='Cost Price in the unit of measure of the product')
    company_currency_id = fields.Many2one(
        related='company_id.currency_id', readonly=True, store=True)
    valuation = fields.Monetary(
        compute='_compute_valuation', currency_field='company_currency_id',
        readonly=True, string='Valuation', store=True)

    @api.onchange('product_id')
    def onchange_product(self):
        res = super(StockInventoryLine, self).onchange_product()
        if self.product_id:
            self.standard_price = self.product_id.standard_price
        return res

    @api.model
    def create(self, vals):
        if vals.get('product_id') and not vals.get('standard_price'):
            product = self.env['product.product'].browse(vals['product_id'])
            vals['standard_price'] = product.standard_price
        return super(StockInventoryLine, self).create(vals)


class StockInventory(models.Model):
    _inherit = 'stock.inventory'

    @api.depends('line_ids.valuation')
    def _compute_valuation(self):
        rg_res = self.env['stock.inventory.line'].read_group(
            [('inventory_id', 'in', self.ids)],
            ['inventory_id', 'valuation'],
            ['inventory_id'])
        mapped_data = dict([(x['inventory_id'][0], x['valuation']) for x in rg_res])
        for inv in self:
            inv.valuation = mapped_data.get(inv.id, 0)

    company_currency_id = fields.Many2one(
        related='company_id.currency_id', readonly=True, store=True)
    valuation = fields.Monetary(
        compute='_compute_valuation', currency_field='company_currency_id',
        readonly=True, string='Valuation')
