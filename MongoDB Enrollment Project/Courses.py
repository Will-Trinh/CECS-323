from mongoengine import *
import mongoengine
from Departments import Department

class Course(Document):

    department = ReferenceField(Department, required=True, reverse_delete_rule=mongoengine.DENY)
    courseNumber = IntField(db_field='course_number', min_value = 100, max_value = 699, required=True)
    courseName = StringField(db_field='course_name', min_length= 1, max_length= 80, required=True)
    description = StringField(db_field='description', min_length = 0, max_length = 80, required = True)
    units = IntField(db_field='units', min_value = 1, max_value = 5, required = True)
    # department = EmbeddedDocumentField(Department, db_field='department')




    meta = {'collection': 'courses',
            'indexes': [
                {'unique': True, 'fields': ['department', 'courseNumber'], 'name': 'courses_uk_01'},
                {'unique': True, 'fields': ['department', 'courseName'], 'name': 'courses_uk_02'}
            ]}
    
    def __init__(self, department: Department, courseNumber: int, courseName: str, description: str, units: int, *args, **values):
        super().__init__(*args, **values)
        self.department = department
        self.courseNumber = courseNumber
        self.courseName = courseName
        self.description = description
        self.units = units


    def __str__(self):
        return (f"Department Abbreviation: {self.department.abbreviation} "
                f"\nnumber: {self.courseNumber}"
                f"\n name: {self.courseName}"
                f"\n units: {self.units}")
