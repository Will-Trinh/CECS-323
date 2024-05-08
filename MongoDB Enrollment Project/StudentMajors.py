from mongoengine import *
import mongoengine
from Majors import Major
from Students import Student
from datetime import datetime

class StudentMajor(Document):

    student = ReferenceField(Student, required=True, reverse_delete_rule=mongoengine.DENY)
    major = ReferenceField(Major, required=True, reverse_delete_rule=mongoengine.DENY)
    declarationDate = DateTimeField(db_field='declarationDate', max_value=datetime.now(), required=True)
    meta = {'collection': 'student_majors',
            'indexes': [
                {'unique': True, 'fields': ['student', 'major'], 'name': 'studentMajors_uk_01'}
            ]}

    def __init__(self, student: str, major: str, declarationDate: datetime, *args, **values):
        super().__init__(*args, **values)
        self.student = student
        self.major = major
        self.declarationDate = declarationDate

    def __str__(self):
        return f"Student major - student: {self.student} major: {self.major}"