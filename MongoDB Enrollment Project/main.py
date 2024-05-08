from ConstraintUtilities import select_general, unique_general, prompt_for_date
from Utilities import Utilities
from CommandLogger import CommandLogger, log
from pymongo import monitoring
from Menu import Menu
from menu_definitions import menu_main, add_select, list_select, select_select, delete_select
from decimal import Decimal, InvalidOperation
from mongoengine.errors import OperationError
from Departments import Department
from Option import Option
from Courses import Course
from Sections import Section
from Students import Student
from Majors import Major
from StudentMajors import StudentMajor
from Enrollments import Enrollment
from PassFails import PassFail
from LetterGrades import LetterGrade
from datetime import datetime
from pprint import pprint

def menu_loop(menu: Menu):
    """Little helper routine to just keep cycling in a menu until the user signals that they
    want to exit.
    :param  menu:   The menu that the user will see."""
    action: str = ''
    while action != menu.last_action():
        action = menu.menu_prompt()
        print('next action: ', action)
        exec(action)

def add():
    menu_loop(add_select)


def list_members():
    menu_loop(list_select)


def select():
    menu_loop(select_select)


def delete():
    menu_loop(delete_select)

def prompt_for_enum(prompt: str, cls, attribute_name: str):
    """
    MongoEngine attributes can be regulated with an enum.  If they are, the definition of
    that attribute will carry the list of choices allowed by the enum (as well as the enum
    class itself) that we can use to prompt the user for one of the valid values.  This
    represents the 'don't let bad data happen in the first place' strategy rather than
    wait for an exception from the database.
    :param prompt:          A text string telling the user what they are being prompted for.
    :param cls:             The class (not just the name) of the MongoEngine class that the
                            enumerated attribute belongs to.
    :param attribute_name:  The NAME of the attribute that you want a value for.
    :return:                The enum class member that the user selected.
    """
    attr = getattr(cls, attribute_name)  # Get the enumerated attribute.
    if type(attr).__name__ == 'EnumField':  # Make sure that it is an enumeration.
        enum_values = []
        for choice in attr.choices:  # Build a menu option for each of the enum instances.
            enum_values.append(Option(choice.value, choice))
        # Build an "on the fly" menu and prompt the user for which option they want.
        return Menu('Enum Menu', prompt, enum_values).menu_prompt()
    else:
        raise ValueError(f'This attribute is not an enum: {attribute_name}')
    

#add functions____________________________    
def add_department():
    """
    creates a department instance
    """
    success: bool = False
    new_department = None
    while not success:
        new_department = Department(
                            input('Name --> '),
                            input('Abbreviation --> '),
                            input('Chair name --> '),
                            input('building --> '),
                            str(input('office --> ')),
                            input('Description --> '))
        violated_constraints = unique_general(new_department)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('try again')
        else:
            try:
                success = True
                new_department.save()
            except Exception as e:
                success = False
                print(e)
                print("Sorry try again.")
            
    

def add_course():
    """
    creates a course instance
    """
    success: bool = False
    new_course = None
    while not success:
        new_course = Course(
                            select_general(Department),
                            int(input('Course number --> ')),
                            input('Course name --> '),
                            input('Description --> '),
                            int(input('units --> ')))
        violated_constraints = unique_general(new_course)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('try again')
        else:
            try:
                success = True
                new_course.save()
            except Exception as e:
                success = False
                print(e)
                print("Sorry try again.")

def add_section():
    """
    creates a section instance
    """
    success: bool = False
    new_section = None
    while not success:
        hour = int(input('Starting time hour --> '))
        minute = int(input('Starting time minute --> '))
        startTime = datetime(1, 1, 1, hour, minute, 0)
        new_section = Section(
                            select_general(Course),
                            int(input('Section number --> ')),
                            input('Semester --> '),
                            int(input('Year --> ')),
                            input('Building --> '),
                            int(input('Room --> ')),
                            input('Schedule --> '),
                            startTime,
                            input('Instructor --> ')
                            )
        violated_constraints = unique_general(new_section)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('try again')
        else:
            try:
                success = True
                new_section.save()
            except Exception as e:
                success = False
                print(e)
                print("Sorry try again.")

def add_student():
    """
    creates a student instance
    """
    success: bool = False
    new_student = None
    while not success:
        new_student = Student(
                            input('Last name --> '),
                            input('First name --> '),
                            input('Email --> '))
        violated_constraints = unique_general(new_student)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('try again')
        else:
            try:
                success = True
                new_student.save()
            except Exception as e:
                success = False
                print(e)
                print("Sorry try again.")

def add_major():
    """
    creates a major instance
    """
    success: bool = False
    new_major = None
    while not success:
        new_major = Major(
                            select_general(Department),
                            input('Name --> '),
                            input('Description --> '))
        violated_constraints = unique_general(new_major)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('try again')
        else:
            try:
                success = True
                new_major.save()
            except Exception as e:
                success = False
                print(e)
                print("Sorry try again.")

def add_student_major():
    """
    creates a Student Major instance
    """
    success: bool = False
    new_student_major = None
    while not success:
        new_student_major = StudentMajor(
                            select_general(Student),
                            select_general(Major),
                            prompt_for_date('Date of assignment --> '))
        violated_constraints = unique_general(new_student_major)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('try again')
        else:
            try:
                success = True
                new_student_major.save()
            except Exception as e:
                success = False
                print(e)
                print("Sorry try again.")

def add_enrollment():
    """
    creates an enrollment instance, and a corresponding passfail or lettegrade to attach to it. if either fails it will delete the other and backout
    """
    success: bool = False
    new_enrollment = None
    while not success:
        new_enrollment = Enrollment(
                            select_general(Section),
                            select_general(Student))
        violated_constraints = unique_general(new_enrollment)
        if len(violated_constraints) > 0:
            for violated_constraint in violated_constraints:
                print('Your input values violated constraint: ', violated_constraint)
            print('try again')
        else:
            try:
                success = True
                new_enrollment.save()
                while True:
                    choice = int(input('What kind of enrollment is this?\n1.PassFail\n2.LetterGrade\n--> '))
                    if choice == 1:
                        new_pass_fail = PassFail(
                                            new_enrollment,
                                            prompt_for_date('Date of application'))
                        violated_constraints = unique_general(new_pass_fail)
                        if len(violated_constraints) > 0:
                            for violated_constraint in violated_constraints:
                                print('Your input values violated constraint: ', violated_constraint)
                            print('try again')
                        else:
                            try:
                                new_pass_fail.save()
                                break
                            except Exception as e:
                                print(e)
                                print("Sorry try again.")  
                    elif choice == 2:
                        new_letter_grade = LetterGrade(
                                            new_enrollment,
                                            input('Minimum satisfacotry grade --> '))
                        violated_constraints = unique_general(new_letter_grade)
                        if len(violated_constraints) > 0:
                            for violated_constraint in violated_constraints:
                                print('Your input values violated constraint: ', violated_constraint)
                            print('try again')
                        else:
                            try:
                                new_letter_grade.save()
                                break
                            except Exception as e:
                                print(e)
                                print("Sorry try again.")
                    else:
                        print('Not a valid option.')
            except Exception as e:
                success = False
                print(e)
                print("Sorry try again.")
            

#delete functions_________________________
def delete_department():
    """
    Delete an existing department
    """
    department = select_general(Department)  # prompt the user for an order to delete
    #will error if there are any children that would be orphaned by the delete, will catch adn print the exception
    try:
        department.delete()
    except Exception as e:
        print(e)


def delete_course():
    """
    Delete an existing course
    """
    course = select_general(Course)  # prompt the user for an order to delete
    #will error if there are any children that would be orphaned by the delete, will catch adn print the exception
    try:
        course.delete()
    except Exception as e:
        print(e)

def delete_section():
    """
    Delete an existing section
    """
    section = select_general(Section)  # prompt the user for an order to delete
    #will error if there are any children that would be orphaned by the delete, will catch adn print the exception
    try:
        section.delete()
    except Exception as e:
        print(e)

def delete_student():
    """
    Delete an existing student
    """
    student = select_general(Student)  # prompt the user for an order to delete
    #will error if there are any children that would be orphaned by the delete, will catch and print the exception
    try:
        student.delete()
    except Exception as e:
        print(e)

def delete_major():
    """
    Delete an existing major
    """
    major = select_general(Major)  # prompt the user for an order to delete
    #will error if there are any children that would be orphaned by the delete, will catch adn print the exception
    try:
        major.delete()
    except Exception as e:
        print(e)

def delete_student_major():
    """
    Delete an existing student major
    """
    studentMajor = select_general(StudentMajor)  # prompt the user for an order to delete
    #will error if there are any children that would be orphaned by the delete, will catch adn print the exception
    try:
        studentMajor.delete()
    except Exception as e:
        print(e)

def delete_enrollment():
    """
    Delete an existing enrollment
    """
    enrollment = select_general(Enrollment)  # prompt the user for an order to delete
    #will error if there are any children that would be orphaned by the delete, will catch adn print the exception
    try:
        enrollment.delete()
    except Exception as e:
        print(e)

#list functions_________________________
def list_department():
    counter = 0
    for department in Department.objects():
        counter += 1
        print(f'{counter}. {department}')

def list_course():
    counter = 0
    for course in Course.objects():
        counter += 1
        print(f'{counter}. {course}')

def list_section():
    counter = 0
    for section in Section.objects():
        counter += 1
        print(f'{counter}. {section}')

def list_student():
    counter = 0
    for student in Student.objects():
        counter += 1
        print(f'{counter}. {student}')

def list_major():
    counter = 0
    for major in Major.objects():
        counter += 1
        print(f'{counter}. {major}')

def list_student_major():
    counter = 0
    for studentMajor in StudentMajor.objects():
        counter += 1
        print(f'{counter}. {studentMajor}')

def list_enrollment():
    counter = 0
    for enrollment in Enrollment.objects():
        counter += 1
        print(f'{counter}. {enrollment}')


if __name__ == '__main__':
    print('Starting in main.')
    monitoring.register(CommandLogger())
    db = Utilities.startup()
    main_action: str = ''
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)
    log.info('All done for now.')
