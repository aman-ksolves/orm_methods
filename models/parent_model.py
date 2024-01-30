from odoo import models, fields, api


class ParentModel(models.Model):
    _name = 'orm_module.parent'
    _description = 'Parent Model'

    name = fields.Char(string='Parent Name', required=True)
    child_ids = fields.One2many('orm_module.child', 'parent_id', string='Children')

    @api.model
    def create(self, values):
        if 'name' in values:
            values['name'] = values['name'].lower()
        return super(ParentModel, self).create(values)

    def write(self, values):
        if 'name' in values:
            values['name'] = values['name'].lower()
        return super(ParentModel, self).write(values)

    # SQL constraints are defined through the model attribute _sql_constraints.
    # This attribute is assigned a list of triples containing strings (name, sql_definition, message)
    # , where name is a valid SQL constraint name, sql_definition is a table_constraint expression
    # and message is the error message.
    _sql_constraints = [
        ('unique_parent_name', 'UNIQUE(name)', 'Parent name must be unique.'),
    ]

    # (0, 0,  { values })    link to a new record that needs to be created with the given values dictionary
    # (1, ID, { values })    update the linked record with id = ID (write *values* on it)
    # (2, ID)                remove and delete the linked record with id = ID (calls unlink on ID, that will delete the object completely, and the link to it as well)
    # (3, ID)                cut the link to the linked record with id = ID (delete the relationship between the two objects but does not delete the target object itself)
    # (4, ID)                link to existing record with id = ID (adds a relationship)
    # (5)                    unlink all (like using (3,ID) for all linked records)
    # (6, 0, [IDs])          replace the list of linked IDs (like using (5) then (4,ID) for each ID in the list of IDs)

    # In your case you need to use (0, 0, { values })
    def create_child_record(self):
        self.write({'child_ids': [(0, 0, {'name': 'New Child'})]})
        # fields.Command.create({'name': 'New Child'})

    def update_parent_name(self):
        # self.write({
        #     'name': [(1, self.id, {'name': 'new Parent Name'})],
        # })
        self.write({
            'name': 'new Parent Name',
        })

    def delete_child_records(self):
        self.write({'child_ids': [(5, 0, 0)]})

    def replace_child_records(self):
        # new_child_ids = [(0, 0, {'name': 'New Child 1'}),
        #                  (0, 0, {'name': 'New Child 2'}),
        #                  (0, 0, {'name': 'New Child 3'})]
        # for rec in new_child_ids:
        #     res = self.env['orm_module.child'].create(rec)
        self.write({'child_ids': [(6, 0, [1, 2, 3])]})

    def custom_function_1(self):
        # delete 2
        # self.write({'child_ids': [(2, 13, 0)]})

        # unlink 3
        # self.write({'child_ids': [(3, 12, 0)]})

        # link 4
        self.write({'child_ids': [(4, 12, 0)]})

    def custom_function_2(self):
        pass

    def test_with_unlink(self):
        parent2 = self.env['orm_module.parent'].create({'name': 'other parent'})

        parent = self.env['orm_module.parent'].create({
            'name': 'test company',
            'child_ids': [
                (0, 0, {'name': 'Child 1'}),
                (0, 0, {'name': 'Child 2'}),
            ]
        })
        child = parent.child_ids[0]
        parent.write({
            # 'country_id': parent2.id,
            'child_ids': [(2, child.id)],
        })
