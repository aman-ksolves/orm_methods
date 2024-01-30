from odoo import models, fields


class ParentModel(models.Model):
    _name = 'orm_module.parent'
    _description = 'Parent Model'

    name = fields.Char(string='Parent Name')
    child_ids = fields.One2many('orm_module.child', 'parent_id', string='Children')

    def create_child_record(self):
        self.write({'child_ids': [(0, 0, {'name': 'New Child'})]})
        # fields.Command.create({'name': 'New Child'})

    def update_parent_name(self):
        self.write({'name': 'Updated Parent Name'})

    def delete_child_records(self):
        self.write({'child_ids': [(5, 0, 0)]})

    def replace_child_records(self):
        new_child_ids = [(0, 0, {'name': 'New Child 1'}),
                         (0, 0, {'name': 'New Child 2'}),
                         (0, 0, {'name': 'New Child 3'})]
        self.write({'child_ids': [(6, 0, new_child_ids)]})

    def custom_function_1(self):
        # Your custom function logic goes here
        self.write({'child_ids': [(3, 12, 0)]})


    def custom_function_2(self):
        # Your custom function logic goes here
        pass