import mongoengine
from mongoengine import *
from Courses import Course
from datetime import datetime

class Section(Document):

    course = ReferenceField(Course, required=True, reverse_delete_rule=mongoengine.DENY)
    sectionNumber = IntField(db_field='section_number', required=True)
    semester = StringField(db_field='semester',choices=('Fall','Spring','Summer I', 'Summer II', 'Summer III', 'Winter'), required=True)
    sectionYear = IntField(db_field='section_year',required=True)
    building = StringField(db_field='building',choices=('ANAC','CDC','DC','ECS','EN2','EN3','EN4','EN5','ET','HSCI','NUR','VEC') ,required=True)
    room = IntField(db_field='room', min_value = 1, max_value = 999, required=True)
    schedule = StringField(db_field='schedule',choices=('MW','TuTh','MWF','F','S'),required=True)
    startTime = DateTimeField(db_field='start_time', min_value=datetime(1, 1, 1, 8, 0, 0), max_value=datetime(1, 1, 1, 19, 30, 0),required=True)
    instructor = StringField(db_field='instructor',required=True)
    meta = {'collection': 'sections',
            'indexes': [
                {'unique': True, 'fields': ['course', 'sectionNumber','semester','sectionYear'], 'name': 'sections_uk_01'},
                {'unique': True, 'fields': ['semester', 'sectionYear','building','room','schedule', 'startTime'], 'name': 'sections_uk_02'},
                {'unique': True, 'fields': ['semester', 'sectionYear', 'schedule', 'startTime', 'instructor'], 'name': 'sections_uk_03'}
            ]}
    
    def __init__(self, course: Course, sectionNumber: int, semester: str, sectionYear: int, building: str, room: int,
                schedule: str, startTime: datetime, instructor: str, *args, **values):
        super().__init__(*args,**values)
        self.course = course
        self.sectionNumber = sectionNumber
        self.building = building
        self.instructor = instructor
        self.room = room
        self.schedule = schedule
        self.startTime = startTime
        self.sectionYear = sectionYear
        self.semester = semester

    def __str__(self):
        return (f"Course number: {self.course.courseNumber} Course name: {self.course.courseName}\n"
                    f"Section number: {self.sectionNumber} Semester: {self.semester} Section year: {self.sectionYear}\n"
                    f"Instructor: {self.instructor} Schedule: {self.schedule} Start time: {self.startTime}\n"
                    f"Building: {self.building} Room: {self.room}")