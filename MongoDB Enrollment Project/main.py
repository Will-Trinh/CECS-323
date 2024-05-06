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
    pass

def add_student():
    pass

def add_major():
    pass

def add_student_major():
    pass

def add_enrollment():
    pass

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
    #will error if there are any children that would be orphaned by the delete, will catch adn print the exception
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
    for x in db.departments.find(): 
        print(x)

def list_course():
    for x in db.courses.find(): 
        print(x)

def list_section():
    for x in db.sections.find(): 
        print(x)

def list_student():
    for x in db.students.find(): 
        print(x)

def list_major():
    for x in db.majors.find(): 
        print(x)

def list_student_major():
    for x in db.student_majors.find(): 
        print(x)

def list_enrollment():
    for x in db.enrollments.find(): 
        print(x)


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
