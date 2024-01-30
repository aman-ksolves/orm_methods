from odoo import models, fields


class ChildModel(models.Model):
    _name = 'orm_module.child'
    _description = 'Child Model'

    name = fields.Char(string='Child Name')
    parent_id = fields.Many2one('orm_module.parent', string='Parent')
