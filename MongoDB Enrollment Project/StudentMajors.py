from mongoengine import *
import mongoengine
from Majors import Major
from Students import Student
from datetime import datetime

class StudentMajor(Document):

    student = StringField(db_field='student', max_length=80, min_length=1, required=True)
    major = StringField(db_field='major', max_length=80, min_length=1, required=True)
    studentId = StringField(db_field='student_id', max_length=80, min_length=1, required=True)
    majorName = StringField(db_field='major_name', max_length=80, min_length=1, required=True)
    declarationDate = DateTimeField(db_field='declarationDate',
                                    max_value=datetime.now(),
                                    required=True)
    meta = {'collection': 'student_majors',
            'indexes': [
                {'unique': True, 'fields': ['student', 'majorName'], 'name': 'studentMajors_uk_01'}
            ]}

    def __init__(self, student: str, major: str, studentId: str, majorName: str, declarationDate: datetime, *args, **values):
        super().__init__(*args, **values)
        self.student = student
        self.major = major
        self.studentId = studentId
        self.majorName = majorName
        self.declarationDate = declarationDate

    def __str__(self):
        return f"Student major - student: {self.student} major: {self.major}"