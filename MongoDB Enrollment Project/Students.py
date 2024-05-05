from mongoengine import *


class Student(Document):
    lastName = StringField(db_field='last_name', max_length=80, min_length=1, required=True)
    firstName = StringField(db_field='first_name', max_length=80, min_length=1, required=True)
    email = StringField(db_field='eMail', max_length=80, min_length=1, required=True)
    
    meta = {'collection': 'students',
            'indexes': [
                {'unique': True, 'fields': ['lastName', 'firstName'], 'name': 'students_uk_01'},
                {'unique': True, 'fields': ['email'], 'name': 'students_uk_02'},
            ]}

    def __init__(self, lastName: str, firstName: str, email: str, *args, **values):
        super().__init__(*args, **values)
        self.lastName = lastName
        self.firstName = firstName
        self.email = email

    def __str__(self):
        return f"Name: {self.lastName}, {self.firstName} e-mail: {self.email}"