import logging
from datetime import time

from constants import *
from menu_definitions import menu_main, add_menu, delete_menu, list_menu, debug_select, introspection_select
from IntrospectionFactory import IntrospectionFactory
from db_connection import engine, Session
from orm_base import metadata
# Note that until you import your SQLAlchemy declarative classes, such as Student, Python
# will not execute that code, and SQLAlchemy will be unaware of the mapped table.
from Department import Department
from Course import Course
from Major import Major
from Student import Student
from StudentMajor import StudentMajor
from Option import Option
from Menu import Menu
from SQLAlchemyUtilities import check_unique
from pprint import pprint
from Section import Section
from Enrollment import Enrollment

def valid_input(prompt: str, valid_entries: tuple | list | set) -> str:
    while True:
        user_input = input(prompt)
        if user_input in valid_entries:
            return user_input
        print(f"Invalid input. Input must only be {valid_entries}.  Try again.")
def add(sess: Session):
    add_action: str = ''
    while add_action != add_menu.last_action():
        add_action = add_menu.menu_prompt()
        exec(add_action)


def delete(sess: Session):
    delete_action: str = ''
    while delete_action != delete_menu.last_action():
        delete_action = delete_menu.menu_prompt()
        exec(delete_action)


def list_objects(sess: Session):
    list_action: str = ''
    while list_action != list_menu.last_action():
        list_action = list_menu.menu_prompt()
        exec(list_action)


def add_department(session: Session):
    """
    Prompt the user for the information for a new department and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """

    while True:
        name = input("Department full name--> ")
        abbreviation = input("Department abbreviation--> ")
        building = input("Department building --> ")
        try:
            office = int(input("Department office--> "))
        except ValueError:
            print("Input an integer: ")
            continue

        description: str = input("Department description--> ")
        chair: str = input("Department chair--> ")

        department: Department = Department(abbreviation, name, chair, building, office, description)

        if check_unique(session, department):
            print(check_unique(session, department))
            print("Try again.")

        else:
            session.add(Department(abbreviation, name, chair, building, office, description))
            return






def add_course_old(session: Session):
    """
    Prompt the user for the information for a new course and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    print("Which department offers this course?")
    department: Department = select_department(sess)
    unique_number: bool = False
    unique_name: bool = False
    number: int = -1
    name: str = ''
    while not unique_number or not unique_name:
        name = input("Course full name--> ")
        number = int(input("Course number--> "))
        name_count: int = session.query(Course).filter(Course.departmentAbbreviation == department.abbreviation,
                                                       Course.name == name).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a course by that name in that department.  Try again.")
        if unique_name:
            number_count = session.query(Course). \
                filter(Course.departmentAbbreviation == department.abbreviation,
                       Course.courseNumber == number).count()
            unique_number = number_count == 0
            if not unique_number:
                print("We already have a course in this department with that number.  Try again.")
    description: str = input('Please enter the course description-->')
    units: int = int(input('How many units for this course-->'))
    course = Course(department, number, name, description, units)
    session.add(course)


def add_course(session: Session):
    """
    This demonstrates how to use the utilities in SQLAlchemy Utilities for checking
    all the uniqueness constraints of a table in one method call.  The user
    experience is tougher to customize using this technique, but the benefit is that
    new uniqueness constraints will be automatically added to the list to be checked,
    without any change to the add_course code.

    Prompt the user for the information for a new course and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    print("Which department offers this course?")
    department: Department = select_department(sess)
    description: str = input('Please enter the course description-->')
    units: int = int(input('How many units for this course-->'))
    violation = True  # Flag that we still have to prompt for fresh values
    while violation:
        name = input("Course full name--> ")
        number = int(input("Course number--> "))
        course = Course(department, number, name, description, units)
        violated_constraints = check_unique(Session, course)
        if len(violated_constraints) > 0:
            print('The following uniqueness constraints were violated:')
            pprint(violated_constraints)
            print('Please try again.')
        else:
            violation = False
    session.add(course)


def add_major(session: Session):
    """
    Prompt the user for the information for a new major and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    print("Which department offers this major?")
    department: Department = select_department(sess)
    unique_name: bool = False
    name: str = ''
    while not unique_name:
        name = input("Major name--> ")
        name_count: int = session.query(Major).filter(Major.departmentAbbreviation == department.abbreviation,
                                                      ).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a major by that name in that department.  Try again.")
    description: str = input('Please give this major a description -->')
    major: Major = Major(department, name, description)
    session.add(major)


def add_student(session: Session):
    """
    Prompt the user for the information for a new student and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    unique_name: bool = False
    unique_email: bool = False
    last_name: str = ''
    first_name: str = ''
    email: str = ''
    while not unique_email or not unique_name:
        last_name = input("Student last name--> ")
        first_name = input("Student first name-->")
        email = input("Student e-mail address--> ")
        name_count: int = session.query(Student).filter(Student.lastName == last_name,
                                                        Student.firstName == first_name).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a student by that name.  Try again.")
        if unique_name:
            email_count = session.query(Student).filter(Student.email == email).count()
            unique_email = email_count == 0
            if not unique_email:
                print("We already have a student with that email address.  Try again.")
    new_student = Student(last_name, first_name, email)
    session.add(new_student)


def add_student_major(sess):
    student: Student = select_student(sess)
    major: Major = select_major(sess)
    student_major_count: int = sess.query(StudentMajor).filter(StudentMajor.studentId == student.studentID,
                                                               StudentMajor.majorName == major.name).count()
    unique_student_major: bool = student_major_count == 0
    while not unique_student_major:
        print("That student already has that major.  Try again.")
        student = select_student(sess)
        major = select_major(sess)
    student.add_major(major)
    """The student object instance is mapped to a specific row in the Student table.  But adding
    the new major to its list of majors does not add the new StudentMajor instance to this session.
    That StudentMajor instance was created and added to the Student's majors list inside of the
    add_major method, but we don't have easy access to it from here.  And I don't want to have to 
    pass sess to the add_major method.  So instead, I add the student to the session.  You would
    think that would cause an insert, but SQLAlchemy is smart enough to know that this student 
    has already been inserted, so the add method takes this to be an update instead, and adds
    the new instance of StudentMajor to the session.  THEN, when we flush the session, that 
    transient instance of StudentMajor gets inserted into the database, and is ready to be 
    committed later (which happens automatically when we exit the application)."""
    sess.add(student)                           # add the StudentMajor to the session
    sess.flush()



def add_major_student(sess):
    major: Major = select_major(sess)
    student: Student = select_student(sess)
    student_major_count: int = sess.query(StudentMajor).filter(StudentMajor.studentId == student.studentID,
                                                               StudentMajor.majorName == major.name).count()
    unique_student_major: bool = student_major_count == 0
    while not unique_student_major:
        print("That major already has that student.  Try again.")
        major = select_major(sess)
        student = select_student(sess)
    major.add_student(student)
    """The major object instance is mapped to a specific row in the Major table.  But adding
    the new student to its list of students does not add the new StudentMajor instance to this session.
    That StudentMajor instance was created and added to the Major's students list inside of the
    add_student method, but we don't have easy access to it from here.  And I don't want to have to 
    pass sess to the add_student method.  So instead, I add the major to the session.  You would
    think that would cause an insert, but SQLAlchemy is smart enough to know that this major 
    has already been inserted, so the add method takes this to be an update instead, and adds
    the new instance of StudentMajor to the session.  THEN, when we flush the session, that 
    transient instance of StudentMajor gets inserted into the database, and is ready to be 
    committed later (which happens automatically when we exit the application)."""
    sess.add(major)                           # add the StudentMajor to the session
    sess.flush()

#Another option in your menu will be to enroll by adding a Student to a Section

def enroll_add_student_section(sess: Session) -> None:
    while True:
        student: Student = select_student(sess)
        section: Section = select_section(sess)
        enrollment: Enrollment = Enrollment(section, student)
        if check_unique(sess, enrollment):
            print("Constraints violated:")
            print(check_unique(sess, enrollment))
            print("Try again.")
        else:
            break
    student.add_section(section)
    sess.add(student)
    sess.flush()


# One option in your menu will be to enroll by adding a Section to a Student.

def enroll_add_section_student(sess: Session) -> None:
    while True:
        section: Section = select_section(sess)
        student: Student = select_student(sess)
        enrollment: Enrollment = Enrollment(section, student)
        if check_unique(sess, enrollment):
            print("Constraints violated:")
            print(check_unique(sess, enrollment))
            print("Try again.")
        else:
            break
    section.add_student(student)
    sess.add(section)
    sess.flush()

# Add_enrollment will ask how you would like to add an enrollment
def add_enrollment(sess):
    while True:
        option:int = int(input("How would you like to add an enrollment: \n"
                               "    1 - Choose a student to enroll in a specific section  \n"
                               "    2 - Choose a specific section to enroll a student in\n"
                               "--> "))

        if (option == 1):
            enroll_add_student_section(sess)
            break
        if (option == 2):
            enroll_add_section_student(sess)
            break
        else:
            print("Invalid option. Try again")


def select_department(sess: Session) -> Department:
    """
    Prompt the user for a specific department by the department abbreviation.
    :param sess:    The connection to the database.
    :return:        The selected department.
    """
    found: bool = False
    abbreviation: str = ''
    while not found:
        abbreviation = input("Enter the department abbreviation--> ")
        abbreviation_count: int = sess.query(Department). \
            filter(Department.abbreviation == abbreviation).count()
        found = abbreviation_count == 1
        if not found:
            print("No department with that abbreviation.  Try again.")
    return_department: Department = sess.query(Department). \
        filter(Department.abbreviation == abbreviation).first()
    return return_department


def select_course(sess: Session) -> Course:
    """
    Select a course by the combination of the department abbreviation and course number.
    Note, a similar query would be to select the course on the basis of the department
    abbreviation and the course name.
    :param sess:    The connection to the database.
    :return:        The selected student.
    """
    found: bool = False
    department_abbreviation: str = ''
    course_number: int = -1
    while not found:
        department_abbreviation = input("Department abbreviation--> ")
        course_number = int(input("Course Number--> "))
        name_count: int = sess.query(Course).filter(Course.departmentAbbreviation == department_abbreviation,
                                                    Course.courseNumber == course_number).count()
        found = name_count == 1
        if not found:
            print("No course by that number in that department.  Try again.")
    course = sess.query(Course).filter(Course.departmentAbbreviation == department_abbreviation,
                                       Course.courseNumber == course_number).first()
    return course


def select_student(sess) -> Student:
    """
    Select a student by the combination of the last and first.
    :param sess:    The connection to the database.
    :return:        The selected student.
    """
    found: bool = False
    last_name: str = ''
    first_name: str = ''
    while not found:
        last_name = input("Student's last name--> ")
        first_name = input("Student's first name--> ")
        name_count: int = sess.query(Student).filter(Student.lastName == last_name,
                                                     Student.firstName == first_name).count()
        found = name_count == 1
        if not found:
            print("No student found by that name.  Try again.")
    student: Student = sess.query(Student).filter(Student.lastName == last_name,
                                                  Student.firstName == first_name).first()
    return student


def select_major(sess) -> Major:
    """
    Select a major by its name.
    :param sess:    The connection to the database.
    :return:        The selected student.
    """
    found: bool = False
    name: str = ''
    while not found:
        name = input("Major's name--> ")
        name_count: int = sess.query(Major).filter(Major.name == name).count()
        found = name_count == 1
        if not found:
            print("No major found by that name.  Try again.")
    major: Major = sess.query(Major).filter(Major.name == name).first()
    return major


def delete_student(session: Session):
    """
    Prompt the user for a student to delete and delete them.
    :param session:     The current connection to the database.
    :return:            None
    """
    student: Student = select_student(session)
    if student.sections:
        print(f"The student is registered in {len(student.sections)} sections. Remove them first.")
    else:
        session.delete(student)



def delete_department(session: Session):
    """
    Prompt the user for a department by the abbreviation and delete it.
    :param session: The connection to the database.
    :return:        None
    """
    print("deleting a department")
    department = select_department(session)
    n_courses = session.query(Course).filter(Course.departmentAbbreviation == department.abbreviation).count()
    if n_courses > 0:
        print(f"Sorry, there are {n_courses} courses in that department.  Delete them first, "
              "then come back here to delete the department.")
    else:
        session.delete(department)


def delete_student_major(sess):
    """Undeclare a student from a particular major.
    :param sess:    The current database session.
    :return:        None
    """
    print("Prompting you for the student and the major that they no longer have.")
    student: Student = select_student(sess)
    major: Major = select_major(sess)
    student.remove_major(major)


def delete_major_student(sess):
    """Remove a student from a particular major.
    :param sess:    The current database session.
    :return:        None
    """
    print("Prompting you for the major and the student who no longer has that major.")
    major: Major = select_major(sess)
    student: Student = select_student(sess)
    major.remove_student(student)


def list_department(session: Session):
    """
    List all departments, sorted by the abbreviation.
    :param session:     The connection to the database.
    :return:            None
    """
    # session.query returns an iterator.  The list function converts that iterator
    # into a list of elements.  In this case, they are instances of the Student class.
    departments: [Department] = list(session.query(Department).order_by(Department.abbreviation))
    for department in departments:
        print(department)


def list_course(sess: Session):
    """
    List all courses currently in the database.
    :param sess:    The connection to the database.
    :return:        None
    """
    # session.query returns an iterator.  The list function converts that iterator
    # into a list of elements.  In this case, they are instances of the Student class.
    courses: [Course] = list(sess.query(Course).order_by(Course.courseNumber))
    for course in courses:
        print(course)


def list_student(sess: Session):
    """
    List all Students currently in the database.
    :param sess:    The current connection to the database.
    :return:
    """
    students: [Student] = list(sess.query(Student).order_by(Student.lastName, Student.firstName))
    for student in students:
        print(student)


def list_major(sess: Session):
    """
    List all majors in the database.
    :param sess:    The current connection to the database.
    :return:
    """
    majors: [Major] = list(sess.query(Major).order_by(Major.departmentAbbreviation))
    for major in majors:
        print(major)


def list_student_major(sess: Session):
    """Prompt the user for the student, and then list the majors that the student has declared.
    :param sess:    The connection to the database
    :return:        None
    """
    student: Student = select_student(sess)
    recs = sess.query(Student).join(StudentMajor, Student.studentID == StudentMajor.studentId).join(
        Major, StudentMajor.majorName == Major.name).filter(
        Student.studentID == student.studentID).add_columns(
        Student.lastName, Student.firstName, Major.description, Major.name).all()
    for stu in recs:
        print(f"Student name: {stu.lastName}, {stu.firstName}, Major: {stu.name}, Description: {stu.description}")


def list_major_student(sess: Session):
    """Prompt the user for the major, then list the students who have that major declared.
    :param sess:    The connection to the database.
    :return:        None
    """
    major: Major = select_major(sess)
    recs = sess.query(Major).join(StudentMajor, StudentMajor.majorName == Major.name).join(
        Student, StudentMajor.studentId == Student.studentID).filter(
        Major.name == major.name).add_columns(
        Student.lastName, Student.firstName, Major.description, Major.name).all()
    for stu in recs:
        print(f"Student name: {stu.lastName}, {stu.firstName}, Major: {stu.name}, Description: {stu.description}")


def move_course_to_new_department(sess: Session):
    """
    Take an existing course and move it to an existing department.  The course has to
    have a department when the course is created, so this routine just moves it from
    one department to another.

    The change in department has to occur from the Course end of the association because
    the association is mandatory.  We cannot have the course not have any department for
    any time the way that we would if we moved it to a new department from the department
    end.

    Also, the change in department requires that we make sure that the course will not
    conflict with any existing courses in the new department by name or number.
    :param sess:    The connection to the database.
    :return:        None
    """
    print("Input the course to move to a new department.")
    course = select_course(sess)
    old_department = course.department
    print("Input the department to move that course to.")
    new_department = select_department(sess)
    if new_department == old_department:
        print("Error, you're not moving to a different department.")
    else:
        # check to be sure that we are not violating the {departmentAbbreviation, name} UK.
        name_count: int = sess.query(Course).filter(Course.departmentAbbreviation == new_department.abbreviation,
                                                    Course.name == course.name).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a course by that name in that department.  Try again.")
        if unique_name:
            # Make sure that moving the course will not violate the {departmentAbbreviation,
            # course number} uniqueness constraint.
            number_count = sess.query(Course). \
                filter(Course.departmentAbbreviation == new_department.abbreviation,
                       Course.courseNumber == course.courseNumber).count()
            if number_count != 0:
                print("We already have a course by that number in that department.  Try again.")
            else:
                course.set_department(new_department)


def select_student_from_list(session):
    """
    This is just a cute little use of the Menu object.  Basically, I create a
    menu on the fly from data selected from the database, and then use the
    menu_prompt method on Menu to display characteristic descriptive data, with
    an index printed out with each entry, and prompt the user until they select
    one of the Students.
    :param session:     The connection to the database.
    :return:            None
    """
    # query returns an iterator of Student objects, I want to put those into a list.  Technically,
    # that was not necessary, I could have just iterated through the query output directly.
    students: [Department] = list(sess.query(Department).order_by(Department.lastName, Department.firstName))
    options: [Option] = []  # The list of menu options that we're constructing.
    for student in students:
        # Each time we construct an Option instance, we put the full name of the student into
        # the "prompt" and then the student ID (albeit as a string) in as the "action".
        options.append(Option(student.lastName + ', ' + student.firstName, student.studentId))
    temp_menu = Menu('Student list', 'Select a student from this list', options)
    # text_studentId is the "action" corresponding to the student that the user selected.
    text_studentId: str = temp_menu.menu_prompt()
    # get that student by selecting based on the int version of the student id corresponding
    # to the student that the user selected.
    returned_student = sess.query(Department).filter(Department.studentId == int(text_studentId)).first()
    # this is really just to prove the point.  Ideally, we would return the student, but that
    # will present challenges in the exec call, so I didn't bother.
    print("Selected student: ", returned_student)


def list_department_courses(sess):
    department = select_department(sess)
    dept_courses: [Course] = department.get_courses()
    print("Course for department: " + str(department))
    for dept_course in dept_courses:
        print(dept_course)


def boilerplate(sess):
    """
    Add boilerplate data initially to jump start the testing.  Remember that there is no
    checking of this data, so only run this option once from the console, or you will
    get a uniqueness constraint violation from the database.
    :param sess:    The session that's open.
    :return:        None
    """
    department: Department = Department('CECS', 'Computer Engineering Computer Science',
                                        'ECS', 'William Trinh', 105, "XD")

    major1: Major = Major(department, 'Computer Science', 'Fun with blinking lights')

    major2: Major = Major(department, 'Computer Engineering', 'Much closer to the silicon')

    student1: Student = Student('Brown', 'David', 'david.brown@gmail.com')

    student2: Student = Student('Brown', 'Mary', 'marydenni.brown@gmail.com')

    student3: Student = Student('Disposable', 'Bandit', 'disposable.bandit@gmail.com')

    course1: Course = Course(department, 101, 'underwater basketweaving', 'we ball', 3)

    course2: Course = Course(department, 299, 'intro to database', 'locked in', 3)

    section1: Section = Section(course1, 3, "Fall", 1989, "ECS", 200,
                                "MW", time(2, 30), "ME!")

    section2: Section = Section(course2, 1, "Spring", 2012, "ECS", 400,
                                "TuTh", time(4, 30), "You")


    student1.add_major(major1)
    student2.add_major(major1)
    student2.add_major(major2)
    sess.add(department)
    sess.add(major1)
    sess.add(major2)
    sess.add(student1)
    sess.add(student2)
    sess.add(student3)
    sess.add(course1)
    sess.add(course2)
    sess.add(section1)
    sess.add(section2)
    sess.flush()                                # Force SQLAlchemy to update the database, although not commit


def session_rollback(sess):
    """
    Give the user a chance to roll back to the most recent commit point.
    :param sess:    The connection to the database.
    :return:        None
    """
    confirm_menu = Menu('main', 'Please select one of the following options:', [
        Option("Yes, I really want to roll back this session", "sess.rollback()"),
        Option("No, I hit this option by mistake", "pass")
    ])
    exec(confirm_menu.menu_prompt())






############################################################## new functions

def select_section(sess) -> Section:

    user_input: int = int(valid_input("Selecting a Section:\n"
                                "  1 - Select by course/section number \n"
                            "  2 - Select by building/room\n"
                            "  3 - Select by instructor\n"
                                "--> ", ('1','2','3')))




    while True:
        try:
            year: int = int(input("Section year-->  "))

            semester: str = valid_input("Section semester-->  ", ("Fall", "Spring", "Winter", "Summer I", "Summer II"))

            schedule: str = valid_input("Schedule-->  ", ("MW", "TuTh", "MWF", "F", "S"))

            start: time = time(*[int(e) for e in input("Section time[HH:MM]--> ").split(":")])

            if user_input == 1:
                course: Course = select_course(sess)
                section_number: int = int(input("Section number--> "))
                section: Section = sess.query(Section).filter(Section.sectionYear == year, Section.semester == semester,
                                                              Section.schedule == schedule,
                                                              Section.startTime == start,
                                                              Section.courseNumber == course.courseNumber,
                                                              Section.departmentAbbreviation == course.departmentAbbreviation,
                                                              Section.sectionNumber == section_number).first()

            elif user_input == 2:
                building: str = valid_input("Section building--> ",
                                                ("VEC", "ECS", "EN2", "EN3", "EN4", "ET", "SSPA"))
                room: int = int(input("Section room number--> "))
                section: Section = sess.query(Section).filter(Section.sectionYear == year, Section.semester == semester,
                                                              Section.schedule == schedule, Section.startTime == start,
                                                              Section.building == building, Section.room == room).first()

            elif user_input == 3:
                instructor: str = input("Section instructor--> ")
                section: Section = sess.query(Section).filter(Section.sectionYear == year, Section.semester == semester,
                                                              Section.schedule == schedule, Section.startTime == start,
                                                              Section.instructor == instructor).first()

            else:
                print("Invalid input. Try again.")

        except ValueError:
            print("Invalid type. Try again.")

        if section:
            print(section)
            return section
        print("This section does not exist. Try again.")







    #select the student you want to unenroll from a section -> remove section from that student
def unenroll_delete_student_section(sess: Session):
    print("Which student do you want to unenroll?")
    select_student(sess).remove_enrollment(select_section(sess))


#select the section you want to uneroll a student from -> remove the student from that section
def unenroll_delete_section_student(sess: Session):
    print("Which section you want to unenroll?")
    select_section(sess).remove_enrollment(select_student(sess))


def delete_enrollment(sess: Session):

    while True:
        user_input: int = int(valid_input("How would you like to delete and enrollment?\n"
                                      "  1 - Unenroll student from section\n"
                                      "  2 - Unenroll section from student\n"
                                          "--> ", ("1", "2")))

        if user_input == 1:
            unenroll_delete_student_section(sess)
            break

        elif user_input == 2:
            unenroll_delete_section_student(sess)
            break



#list sections a student is enrolled in
def list_students_in_section(sess: Session) -> None:
    [print(enrollment.section) for enrollment in select_student(sess).sections]


#list students enrolled in a section
def list_sections_in_student(sess: Session) -> None:
    [print(enrollment.student) for enrollment in select_section(sess).students]

def list_enrollment(sess: Session):
    print("  1 - List all of a student's enrollments")
    print("  2 - List all students in a section")

    try:
        selection: int = int(valid_input("--> ", ('1', '2')))

        if selection == 1:
            ##select student
            student: Student = select_student(sess)
            recs = sess.query(Student).join(Enrollment, Student.studentID == Enrollment.studentID).join(
                Section, Enrollment.sectionID == Section.sectionID).filter(
                Student.studentID == student.studentID).add_columns(
                Student.lastName, Student.firstName, Section.departmentAbbreviation, Section.courseNumber, Section.sectionYear,
                Section.semester, Section.sectionNumber).all()

        elif selection == 2:
            section: Section = select_section(sess)
            recs = sess.query(Section).join(Enrollment, Section.sectionID == Enrollment.sectionID).join(
                Student, Enrollment.studentID == Student.studentID).filter(
                Section.sectionID == section.sectionID).add_columns(
                Student.lastName, Student.firstName, Section.departmentAbbreviation, Section.courseNumber, Section.sectionYear,
                Section.semester, Section.sectionNumber).all()

        for stu in recs:
            print(f"Student name: {stu.lastName}, {stu.firstName}, Department Abbreviation: {stu.departmentAbbreviation} "
                  f"Course Number: {stu.courseNumber}, Year: {stu.sectionYear}, Semester: {stu.semester}, "
                  f"Number: {stu.sectionNumber}")

    except ValueError:
        print("Invalid input. Try again. ")


def add_section(sess: Session):
    """
    Prompt the user for the information for a new section and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    while True:

        course: Course(select_course(Session))


        try:

            number: int = int(input("Section number--> "))
            semester: str = input("Semester--> ")
            year: int = int(input("Section Year --> "))
            building: str = input("Section building--> ")
            room: str = int(input("Room number--> "))
            startTime: time = time(input("Start time--> "))
            instructor: str = input("Instructor--> ")

        except ValueError:
            print("Wrong type.")
            continue



        section: Section = Section(course, number, semester, year, building, room, startTime, instructor)

        if check_unique(sess, section):
            print(check_unique(sess, section))
            print("Try again.")

        else:
            sess.add(Section(course, number, semester, year, building, room, startTime, instructor))
            sess.flush()
            return

def delete_section(sess: Session):
    section: Section = select_section(sess)
    if section.students:
        print(f"This section contains {len(section.students)} students. Remove them first to delete this section.")
    else:
        sess.delete(section)

def delete_course(sess:Session):
    print("Deleting a course")
    course = select_course(sess)
    n_sections = sess.query(Section).filter(course.courseNumber == Section.courseNumber).count()
    if n_sections > 0:
        print("You must delete all sections before deleting a course.")
    else:
        sess.delete(course)


if __name__ == '__main__':
    print('Starting off')
    logging.basicConfig()
    # use the logging factory to create our first logger.
    # for more logging messages, set the level to logging.DEBUG.
    # logging_action will be the text string name of the logging level, for instance 'logging.INFO'
    logging_action = debug_select.menu_prompt()
    # eval will return the integer value of whichever logging level variable name the user selected.
    logging.getLogger("sqlalchemy.engine").setLevel(eval(logging_action))
    # use the logging factory to create our second logger.
    # for more logging messages, set the level to logging.DEBUG.
    logging.getLogger("sqlalchemy.pool").setLevel(eval(logging_action))

    # Prompt the user for whether they want to introspect the tables or create all over again.
    introspection_mode: int = IntrospectionFactory().introspection_type
    if introspection_mode == START_OVER:
        print("starting over")
        # create the SQLAlchemy structure that contains all the metadata, regardless of the introspection choice.
        metadata.drop_all(bind=engine)  # start with a clean slate while in development


        # Create whatever tables are called for by our "Entity" classes that we have imported.
        metadata.create_all(bind=engine)
    elif introspection_mode == REUSE_NO_INTROSPECTION:
        print("Assuming tables match class definitions")

    menu: Menu = menu_main.menu_prompt()
    with Session() as sess:
        action: str = ''
        while (action != menu.last_action()):
            action = menu.menu_prompt()


            ## adding option to go back to main menu from our add, list, and delete menus
            if action == "back":
                menu: Menu = menu_main.menu_prompt()
                continue
            ##############################################################################

            print('next action: ', action)
            exec(action)
        sess.commit()
    print('Ending normally')


 #little helper

