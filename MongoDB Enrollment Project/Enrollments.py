from mongoengine import *
import mongoengine
from Students import Student
from Sections import Section


class Enrollment(Document):

    section = ReferenceField(Section, required=True, reverse_delete_rule=mongoengine.DENY)
    student = ReferenceField(Student, required=True, reverse_delete_rule=mongoengine.DENY)
    departmentAbbreviation = StringField(db_field='abbreviation', max_length=6, min_length=1, required=True)
    courseNumber = IntField(db_field='course_number', min_value = 100, max_value = 699, required=True)
    sectionYear = IntField(db_field='section_year',required=True)
    semester = StringField(db_field='semester',choice=('Fall','Spring','Summer I', 'Summer II', 'Summer III', 'Winter'), required=True)

    meta = {'collection': 'enrollments',
            'indexes': [
                {'unique': True, 'fields': ['student', 'section'], 'name': 'enrollments_uk_01'},
                {'unique': True, 'fields': ['semester', 'sectionYear', 'departmentAbbreviation', 'courseNumber', 'student'], 'name': 'enrollments_uk_02'},
            ]}

    def __init__(self, section:Section, student:Student, *args, **values):
        super().__init__(*args, **values)
        self.section = section
        self.student = student
        self.departmentAbbreviation = self.section.course.department.abbreviation
        self.courseNumber = self.section.course.courseNumber
        self.sectionYear = self.section.sectionYear
        self.semester = self.section.semester
        


    def __str__(self):
        return (f"Enrollment:"
                f"\nStudent: {self.student.firstName} {self.student.lastName}"
                f"\nSection: {self.section}")
