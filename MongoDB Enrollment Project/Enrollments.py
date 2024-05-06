from mongoengine import *
import mongoengine
from Students import Student
from Sections import Section


class Enrollment(Document):

    student = ReferenceField(Student, required=True, reverse_delete_rule=mongoengine.DENY)
    section = ReferenceField(Section, required=True, reverse_delete_rule=mongoengine.DENY)

    meta = {'collection': 'enrollments',
            'indexes': [
                {'unique': True, 'fields': ['student', 'section'], 'name': 'enrollments_uk_01'}
            ]}

    def __init__(self, section:Section, student:Student, *args, **values):
        super().__init__(*args, **values)
        self.section = section
        self.student = student


    def __str__(self):
        return (f"Enrollment:"
                f"\nStudent: {self.student.firstName} {self.student.lastName}"
                f"\nSection: {self.section}")
