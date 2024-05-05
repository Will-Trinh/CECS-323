import mongoengine
from mongoengine import *
from Courses import Course
from datetime import datetime

class Section(Document):

    section_number = IntField(db_field='section_number', required=True)
    semester = StringField(db_field='semester',choice=('Fall','Spring','Summer I', 'Summer II', 'Summer III', 'Winter'), required=True)
    section_year = IntField(db_field='section_year',required=True)
    building = StringField(db_field='building',choices=('ANAC','CDC','DC','ECS','EN2','EN3','EN4','EN5','ET','HSCI','NUR','VEC') ,required=True)
    room = IntField(db_field='room', min_value = 1, max_value = 999, required=True)
    schedule = StringField(db_field='schedule',choices=('MW','TuTh','MWF','F','S'),required=True)
    start_time = DateTimeField(db_field='start_time',required=True)
    instructor = StringField(db_field='instructor',required=True)
    course = ReferenceField(Course, required=True, reverse_delete_rule=mongoengine.DENY)
    
    meta = {'collection': 'sections',
            'indexes': [
                {'unique': True, 'fields': ['course', 'section_number','semester','section_year'], 'name': 'sections_uk_01'},
                {'unique': True, 'fields': ['semester', 'section_year','building','room','schedule', 'start_time'], 'name': 'sections_uk_02'},
                {'unique': True, 'fields': ['semester', 'section_year', 'schedule', 'start_time', 'instructor'], 'name': 'sections_uk_03'}
            ]}
    
    def __init__(self, course: Course, section_number: int, semester: str, section_year: int, building: str, room: int,
                schedule: datetime, start_time: datetime, instructor: str, *args, **values):
        super().__init__(*args,**values)
        self.course = course
        self.section_number = section_number
        self.building = building
        self.instructor = instructor
        self.room = room
        self.schedule = schedule
        self.start_time = start_time
        self.section_year = section_year
        self.semester = semester

    def __str__(self):
        return (f"Course number: {self.courseNumber} Course name: {self.course.name}\n"
                    f"Section number: {self.sectionNumber} Semester: {self.semester} Section year: {self.sectionYear}\n"
                    f"Instructor: {self.instructor} Schedule: {self.schedule} Start time: {self.startTime}\n"
                    f"Building: {self.building} Room: {self.room}")