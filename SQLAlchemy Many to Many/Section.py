from orm_base import Base
from IntrospectionFactory import IntrospectionFactory
from sqlalchemy import UniqueConstraint, ForeignKeyConstraint, CheckConstraint
from sqlalchemy import String, Integer, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Course import Course
from constants import START_OVER, REUSE_NO_INTROSPECTION
from typing import List
from Enrollment import Enrollment

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

        sectionNumber: Mapped[int] = mapped_column('section_number', Integer,
                                                  nullable=False, primary_key=True)

        semester: Mapped[str] = mapped_column('semester', String(10),
                                              CheckConstraint("semester IN('Fall', 'Spring', 'Winter', '"
                                                              "Summer I', 'Summer II')",
                                                              name="semester_name_value_check"), nullable=False,
                                              primary_key=True)

        sectionYear: Mapped[int] = mapped_column('section_year', Integer, nullable=False,
                                                  primary_key=True)

        building: Mapped[str] = mapped_column('building', String(6),
                                              CheckConstraint("building IN('EC', 'ECS', 'EN2', 'EN3', \
                                                'EN4', 'ET', 'SSPA')", name="building_name_value_check"),
                                              nullable=False)

        room: Mapped[int] = mapped_column('room', Integer, nullable=False)


        schedule: Mapped[str] = mapped_column('schedule', String(6),
                                              CheckConstraint("schedule IN('MW', 'TuTh', 'MWF', 'F', 'S')",
                                              name="schedule_name_value_check"), nullable=False)

        startTime: Mapped[Time] = mapped_column('start_time', Time, nullable=False)

        instructor: Mapped[str] = mapped_column('instructor', String(80), nullable=False)

        students : Mapped[List["Enrollment"]] = relationship(back_populates="section",
                                                             cascade="all, save-update, delete-orphan")

        candidate_keys = (UniqueConstraint("section_year", "semester", "schedule", "start_time",
                                           "building", "room", name="sections_uk_01"),
                          UniqueConstraint("section_year", "semester", "schedule", "start_time",
                                           "instructor", name="sections_uk_02"),
                          ForeignKeyConstraint([departmentAbbreviation, courseNumber],
                                               [Course.departmentAbbreviation, Course.courseNumber]))

        def __init__(self, course: Course, sectionNumber: int, semester: str, sectionYear: int,
                     building: str, room: int, schedule: str, startTime: Time, instructor: str):
            self.course = course
            self.sectionNumber = sectionNumber
            self.courseNumber = course.courseNumber
            self.departmentAbbreviation = course.departmentAbbreviation
            self.semester = semester
            self.sectionYear = sectionYear
            self.building = building
            self.room = room
            self.schedule = schedule
            self.startTime = startTime
            self.instructor = instructor

            def add_student(self, student):
                if student in [student for student in self.students]:
                    print("Provided Student already exists in this Section.")
                    return
                section_student = Enrollment(self, student)
                student.sections.append(section_student)
                self.students.append(section_student)

            def remove_enrollment(self, student):
                if student not in [student.student for student in self.students]:
                    print("Provided Student does not exist in this Section.")
                    return
                self.students.pop([student.student for student in self.students].index(student))

            def __str__(self):
                return (f"Course number: {self.courseNumber} Course name: {self.course.name}\n"
                        f"Section number: {self.sectionNumber} Semester: {self.semester} Section year: {self.sectionYear}\n"
                        f"Instructor: {self.instructor} Schedule: {self.schedule} Start time: {self.startTime}\n"
                        f"Building: {self.building} Room: {self.room}")