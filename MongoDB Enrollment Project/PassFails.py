from mongoengine import *
from datetime import *

class PassFail(Document):

    enrollment = ObjectIdField(db_field='enrollment', required=True)
    applicationDate = DateField(db_field='application_date', min_value= datetime.now, required=True)


    meta = {'collection': 'passFails',
            'indexes': [
                {'unique': True, 'fields': ['enrollment'], 'name': 'passFails_uk_01'}
            ]}
    
    def __init__(self, enrollment, applicationDate: date, *args, **values):
        super().__init__(*args, **values)
        self.enrollment = enrollment
        self.applicationDate = applicationDate


    def __str__(self):
        return (f'Enrollment ID: {self.enrollment}\n'
                f'Application Date: {self.applicationDate}')
    
