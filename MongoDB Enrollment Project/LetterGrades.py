from mongoengine import *
import mongoengine
from Enrollments import Enrollment

class LetterGrade(Document):

    enrollment = ReferenceField(Enrollment, required=True, reverse_delete_rule=CASCADE)
    minSatisfactory = StringField(db_field='min_satisfacory',choice=('A', 'B', 'C'), required=True)
    
    meta = {'collection': 'letter_grades',
            'indexes': [
                {'unique': True, 'fields': ['enrollment'], 'name': 'LetterGrade_uk_01'}
            ]}

    def __init__(self, enrollment:Enrollment, minSatisfactory:str, *args, **values):
        super().__init__(*args, **values)
        self.enrollment = enrollment
        self.minSatisfactory = minSatisfactory

    def __str__(self):
        return (f"Letter Grade:"
                f"\nenrollment: {self.enrollment}"
                f"\nminimum satisfactory grade: {self.minSatisfactory}")