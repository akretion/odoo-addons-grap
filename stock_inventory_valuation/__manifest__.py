# -*- coding: utf-8 -*-
# © 2013-Today GRAP (http://www.grap.coop)
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Stock Inventory - Valuation',
    'version': '10.0.1.0.0',
    'category': 'Stock',
    'description': """
Stores the product standard price on the inventory.line, so as to be able to
calculate the total valuation of an inventory.
============================================================================
===============================================

Copyright, Author and Licence :
-------------------------------
    * Copyright : 2014, Groupement Régional Alimentaire de Proximité;
    * Author :
        * Julien WESTE;
        * Sylvain LE GAL (https://twitter.com/legalsylvain);
        * Alexis de Lattre <alexis.delattre@akretion.com>
    * Licence : AGPL-3 (http://www.gnu.org/licenses/)
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': ['stock'],
    'data': ['views/stock_inventory.xml'],
}
