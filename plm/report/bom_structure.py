## -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

'''
Created on Apr 14, 2016

@author: Daniel Smerghetto
'''

from odoo import api
from odoo import models
from odoo.osv import osv
from odoo.report import report_sxw
from operator import itemgetter
from odoo import _
import odoo
import time
import logging


def _translate(value):
    return _(value)


def get_bom_report(myObject, recursion=False, flat=False, leaf=False, level=1, summarize=False):

    def getBom(bomLineObj):
        newBom = None
        for bomBws in bomLineObj.related_bom_ids:
            if bomBws.type == bomLineObj.type:
                newBom = bomBws
                break
        return newBom

    def getOutLineInfos(bomLineBrws, productTmplBrws, prodQty):
        res = {}
        res['row_bom_line'] = bomLineBrws
        res['name'] = productTmplBrws.engineering_code
        res['item'] = bomLineBrws.itemnum
        res['pname'] = productTmplBrws.engineering_code
        res['pdesc'] = _(productTmplBrws.description)
        res['pcode'] = bomLineBrws.product_id.default_code
        res['previ'] = productTmplBrws.engineering_revision
        res['pqty'] = prodQty
        res['uname'] = bomLineBrws.product_uom_id.name
        res['pweight'] = productTmplBrws.weight
        res['code'] = bomLineBrws.product_id.default_code
        res['level'] = level
        res['prodBrws'] = bomLineBrws.product_id
        res['prodTmplBrws'] = productTmplBrws
        res['lineBrws'] = bomLineBrws
        return res

    def leafComputeRecursion(bomObj, parentQty=1):
        for l in bomObj.bom_line_ids:
            lineQty = l.product_qty
            productTmplObj = l.product_id.product_tmpl_id
            prodTmlId = productTmplObj.id
            prodQty = parentQty * lineQty
            myNewBom = getBom(l)
            if myNewBom:
                leafComputeRecursion(myNewBom, prodQty)
            else:
                if prodTmlId not in leafRes.keys():
                    resDict = getOutLineInfos(l, productTmplObj, prodQty)
                    resDict['engineering_code'] = productTmplObj.engineering_code
                    resDict['level'] = ''
                    leafRes[prodTmlId] = resDict
                else:
                    leafRes[prodTmlId]['pqty'] = leafRes[prodTmlId]['pqty'] + prodQty
    if leaf:
        leafRes = {}
        leafComputeRecursion(myObject)
        return leafRes.values()

    def summarize_level(bomObj, recursion=False, flat=False, level=1, summarize=False, parentQty=1):
        def updateQty(tmplId, qtyToAdd):
            for localIndex, valsList in orderDict.items():
                count = 0
                for res in valsList:
                    tmplBrws = res.get('prodTmplBrws', False)
                    if not tmplBrws:
                        logging.error('Template browse not found printing bom: %r' % (res))
                        continue
                    if tmplBrws.id == tmplId:
                        newQty = orderDict[localIndex][count]['pqty'] + qtyToAdd
                        orderDict[localIndex][count]['pqty'] = newQty
                        return
                    count = count + 1

        orderDict = {}
        levelListed = []
        for l in bomObj.bom_line_ids:
            index = l.itemnum
            if index not in orderDict.keys():
                orderDict[index] = []
            children = {}
            productTmplObj = l.product_id.product_tmpl_id
            prodTmlId = productTmplObj.id
            if recursion or flat:
                myNewBom = getBom(l)
                if myNewBom:
                    children = summarize_level(myNewBom, recursion, flat, level + 1, summarize, l.product_qty * parentQty)
            if prodTmlId in levelListed and summarize:
                qty = l.product_qty
                updateQty(prodTmlId, qty)
            else:
                prodQty = l.product_qty
                res = getOutLineInfos(l, productTmplObj, prodQty)
                if productTmplObj.engineering_code:
                    res['engineering_code'] = '- ' * str(level) + ' ' + productTmplObj.engineering_code
                else:
                    res['engineering_code'] = '- ' * str(level) + ' '
                res['children'] = children
                res['level'] = level
                levelListed.append(prodTmlId)
                orderDict[index].append(res)
        return orderDict

    out = []

    def getOutList(outDict, parentQty=1):
        itemNums = outDict.keys()
        itemNums.sort()
        for itemNum in itemNums:
            valsDict = outDict.get(itemNum, {})
            for valDict in valsDict:
                children = valDict.get('children', {}).copy()
                localQty = valDict['pqty']
                if flat:
                    localQty = localQty * parentQty
                    valDict['pqty'] = localQty
                del valDict['children']
                out.append(valDict)
                getOutList(children, localQty)

    outDict = summarize_level(myObject, recursion, flat, level, summarize)
    getOutList(outDict)
    return out


def BomSort(myObject):
    valid = False
    bomobject = []
    res = {}
    index = 0
    for l in myObject:
        res[str(index)] = l.itemnum
        index += 1
        if l.itemnum > 0:
            valid = True
    if not valid:
        res = {}
        index = 0
        for l in myObject:
            res[str(index)] = l.product_id.product_tmpl_id.name
            index += 1
    items = res.items()
    items.sort(key=itemgetter(1))
    for res in items:
        bomobject.append(myObject[int(res[0])])
    return bomobject


class bom_structure_all_custom_report(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(bom_structure_all_custom_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_children': self.get_children,
            'bom_type': self.bom_type,
            'trans': _translate,
            'context': context,
        })

    def get_children(self, myObject, level=0):
        return get_bom_report(myObject, recursion=True, flat=False, leaf=False, level=1, summarize=False)

    def bom_type(self, myObject):
        result = dict(myObject.fields_get()['type']['selection']).get(myObject.type, '')
        return _(result)


class bom_structure_one_custom_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(bom_structure_one_custom_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_children': self.get_children,
            'bom_type': self.bom_type,
            'trans': _translate,
            'context': context,
        })

    def get_children(self, myObject, level=0):
        return get_bom_report(myObject, recursion=False, flat=False, leaf=False, level=1, summarize=False)

    def bom_type(self, myObject):
        result = dict(myObject.fields_get()['type']['selection']).get(myObject.type, '')
        return _(result)


class bom_structure_all_sum_custom_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(bom_structure_all_sum_custom_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_children': self.get_children,
            'bom_type': self.bom_type,
            'trans': _translate,
            'context': context,
        })

    def get_children(self, myObject, level=1):
        return get_bom_report(myObject, recursion=True, flat=False, leaf=False, level=level, summarize=True)

    def bom_type(self, myObject):
        result = dict(myObject.fields_get()['type']['selection']).get(myObject.type, '')
        return _(result)


class bom_structure_one_sum_custom_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(bom_structure_one_sum_custom_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_children': self.get_children,
            'bom_type': self.bom_type,
            'trans': _translate,
            'context': context,
        })

    def get_children(self, myObject):
        return get_bom_report(myObject, summarize=True)

    def bom_type(self, myObject):
        result = dict(myObject.fields_get()['type']['selection']).get(myObject.type, '')
        return _(result)


class bom_structure_leaves_custom_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(bom_structure_leaves_custom_report, self).__init__(cr, uid, name, context=context)
        self.keyIndex = 0
        self.localcontext.update({
            'time': time,
            'get_children': self.get_children,
            'bom_type': self.bom_type,
            'trans': _translate,
            'context': context,
        })

    def get_children(self, myObject, level=1):
        return get_bom_report(myObject, leaf=True, level=level, summarize=True)

    def bom_type(self, myObject):
        result = dict(myObject.fields_get()['type']['selection']).get(myObject.type, '')
        return _(result)


class bom_structure_flat_custom_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(bom_structure_flat_custom_report, self).__init__(cr, uid, name, context=context)
        self.keyIndex = 0
        self.localcontext.update({
            'time': time,
            'get_children': self.get_children,
            'bom_type': self.bom_type,
            'trans': _translate,
            'context': context,
        })

    def get_children(self, myObject, level=1):
        return get_bom_report(myObject, recursion=True, flat=True, leaf=False, level=level, summarize=True)

    def bom_type(self, myObject):
        result = dict(myObject.fields_get()['type']['selection']).get(myObject.type, '')
        return _(result)


class report_plm_bom_all(osv.AbstractModel):
    _name = 'report.plm.bom_structure_all'
    _inherit = 'report.abstract_report'
    _template = 'plm.bom_structure_all'
    _wrapped_report_class = bom_structure_all_custom_report


class report_plm_bom_one(osv.AbstractModel):
    _name = 'report.plm.bom_structure_one'                          # May it is equal to "_template" keyword
    _inherit = 'report.abstract_report'                             # Every time inherit from abstract report
    _template = 'plm.bom_structure_one'                             # Searched as "report_name" in ir.actions.act.window
    _wrapped_report_class = bom_structure_one_custom_report


class report_plm_bom_all_sum(osv.AbstractModel):
    _name = 'report.plm.bom_structure_all_sum'
    _inherit = 'report.abstract_report'
    _template = 'plm.bom_structure_all_sum'
    _wrapped_report_class = bom_structure_all_sum_custom_report


class report_plm_bom_one_sum(osv.AbstractModel):
    _name = 'report.plm.bom_structure_one_sum'
    _inherit = 'report.abstract_report'
    _template = 'plm.bom_structure_one_sum'
    _wrapped_report_class = bom_structure_one_sum_custom_report


class report_plm_bom_leaves_sum(osv.AbstractModel):
    _name = 'report.plm.bom_structure_leaves'
    _inherit = 'report.abstract_report'
    _template = 'plm.bom_structure_leaves'
    _wrapped_report_class = bom_structure_leaves_custom_report


class report_plm_bom_flat(osv.AbstractModel):
    _name = 'report.plm.bom_structure_flat'
    _inherit = 'report.abstract_report'
    _template = 'plm.bom_structure_flat'
    _wrapped_report_class = bom_structure_flat_custom_report
