from email._header_value_parser import Section

from orm_base import Base
from db_connection import engine
from IntrospectionFactory import IntrospectionFactory
from sqlalchemy import UniqueConstraint, ForeignKeyConstraint, CheckConstraint
from sqlalchemy import String, Integer, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property
from sqlalchemy import Table
from Course import Course
from constants import START_OVER, REUSE_NO_INTROSPECTION, INTROSPECT_TABLES


introspection_type = IntrospectionFactory().introspection_type
if introspection_type == START_OVER or introspection_type == REUSE_NO_INTROSPECTION:
    class Section(Base):
        """
        A single instance of a course offered by a university department that students can
        enroll in. Instances are individualized with a specific two digit integer. An example
        would be: Section 01 of CECS 323.
        """
        __tablename__ = "sections"

        departmentAbbreviation: Mapped[str] = mapped_column('department_abbreviation',
                                                            String(10),nullable=False,primary_key=True)

        course: Mapped["Course"] = relationship(back_populates="sections")

        courseNumber: Mapped[int] = mapped_column('course_number', Integer,
                                                  nullable=False, primary_key=True)

        sectionNumber: Mapped[int] = mapped_column('course_number', Integer,
                                                  nullable=False, primary_key=True)

        semester: Mapped[str] = mapped_column('semester', String(10),
                                              CheckConstraint("semester IN('MW', 'TuTh', 'MWF', 'F', 'S')",
                                              name="semester_name_value_check"), nullable=False, primary_key=True)

        sectionYear: Mapped[int] = mapped_column('section_year', Integer, nullable=False,
                                                  primary_key=True)

        building: Mapped[str] = mapped_column('building', String(6),
                                              CheckConstraint("building IN('EC', 'ECS', 'EN2', 'EN3', \
                                                'EN4', 'ET', 'SSPA')", name="semester_name_value_check"),
                                              nullable=False)

        room: Mapped[int] = mapped_column('room', Integer, nullable=False)

        schedule: Mapped[str] = mapped_column('schedule', String(6), nullable=False)

        startTime: Mapped[Time] = mapped_column('start_time', Time, nullable=False)

        instructor: Mapped[str] = mapped_column('instructor', String(80), nullable=False)

        candidate_keys = (UniqueConstraint("section_year", "semester", "schedule", "start_time",
                                           "building", "room", name="sections_uk_01"),
                          UniqueConstraint("section_year", "semester", "schedule", "start_time",
                                           "instructor", name="sections_uk_02"),
                          ForeignKeyConstraint([departmentAbbreviation, courseNumber],
                                               [Course.departmentAbbreviation, Course.courseNumber]))


        def __init__(self,course: Course, sectionNumber: int, semester: str, sectionYear: int,
             building: str, room: int, schedule: str, startTime: Time, instructor: str):

            self.departmentAbbreviation = course.departmentAbbreviation
            self.course = course
            self.courseNumber = course.courseNumber
            self.sectionNumber = sectionNumber
            self.semester = semester
            self.sectionYear = sectionYear
            self.building = building
            self.room = room
            self.schedule = schedule
            self.startTime = startTime
            self.instructor = instructor


        def __str__(self):
            return (f"Course: {self.courseNumber} {self.course.name} {self.sectionNumber} \n"
                    f"Semester: {self.semester} Section year: {self.sectionYear} Instructor: {self.instructor} \n" 
                    f"Schedule: {self.schedule} at  {self.startTime} Location: {self.building} {self.room} \n")

        setattr(Section, "__init__", __init__)
        setattr(Section, "__str__", __str__)