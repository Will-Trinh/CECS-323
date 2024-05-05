from mongoengine import *
import mongoengine
from Departments import Department

class Major(Document):

    department = ReferenceField(Department, required=True, reverse_delete_rule=mongoengine.DENY)
    name = StringField(db_field='name', max_length=40, min_length=5, required=True)
    description = StringField(db_field='description', max_length=80, min_length=1, required=True)

    meta = {'collection': 'majors',
            'indexes': [
                {'unique': True, 'fields': ['name'], 'name': 'majors_uk_01'}
            ]}
    
    def __init__(self, department: Department, name: str, description: str, *args, **values):
        super().__init__(*args, **values)
        self.department = department
        self.name = name 
        self.description = description

    def __str__(self):
        return f'Major: Department: {self.department.abbreviation}, name: {self.name}, Description: {self.description}'