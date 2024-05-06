from mongoengine import *

class Department(Document):

    name = StringField(db_field='name', max_length=80, min_length=1, required=True)
    abbreviation = StringField(db_field='abbreviation', max_length=6, min_length=1, required=True)
    chairName = StringField(db_field='chair_name', max_length=80, min_length=1, required=True)
    building = StringField(db_field='building', required=True, choices=('ANAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3', 'EN4', 'EN5', 'ET', 'HSCI', 'NUR', 'VEC'))
    office = IntField(db_field='office', min_value=1, required=True)
    description = StringField(db_field='description', max_length=80, min_length=1, required=True)

    meta = {'collection': 'departments',
            'indexes': [
                {'unique': True, 'fields': ['name'], 'name': 'departments_uk_01'},
                {'unique': True, 'fields': ['abbreviation'], 'name': 'departments_uk_02'},
                {'unique': True, 'fields': ['chairName'], 'name': 'departments_uk_03'},
                {'unique': True, 'fields': ['building', 'office'], 'name': 'departments_uk_04'}
            ]}
    
    def __init__(self, name: str, abbreviation: str, chairName: str, building: str, office: int, description: str, *args, **values):
        super().__init__(*args, **values)
        self.name = name
        self.abbreviation = abbreviation
        self.chairName = chairName
        self.building = building
        self.office = office
        self.description = description

    def __str__(self):
         return f'Department: name: {self.name}, Abbreviation: {self.abbreviation}, Chair: {self.chairName}, Location: {self.building} {str(self.office)}, Description: {self.description}'