from orm_base import Base
from db_connection import engine
from IntrospectionFactory import IntrospectionFactory
from sqlalchemy import UniqueConstraint, ForeignKeyConstraint
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

        departmentAbbreviation: Mapped[str] = mapped_column('department_abbrevviation',
                                                            String(10),nullable=False,primary_key=True)
        course: Mapped["Course"] = relationship(back_populates="sections")
        courseNumber: Mapped[int] = mapped_column('course_number', Integer,
                                                  nullable=False, primary_key=True)
        sectionNumber: Mapped[int] = mapped_column('course_number', Integer,
                                                  nullable=False, primary_key=True)
