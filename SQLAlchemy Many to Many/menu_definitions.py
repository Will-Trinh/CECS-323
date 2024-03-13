from Menu import Menu
from Option import Option
from constants import *
"""
This little file just has the menus declared.  Each variable (e.g. menu_main) has 
its own set of options and actions.  Although, you'll see that the "action" could
be something other than an operation to perform.

Doing the menu declarations here seemed like a cleaner way to define them.  When
this is imported in main.py, these assignment statements are executed and the 
variables are constructed.  To be honest, I'm not sure whether these are global
variables or not in Python.
"""

# The main options for operating on Departments and Courses
"""menu_main = Menu('main', 'Please select one of the following options:', [
    Option("Add department", "add_department(sess)"),
    Option("Add course", "add_course(sess)"),
    Option("Add section", "add_section(sess)"),
    Option("Delete department", "delete_department(sess)"),
    Option("Delete course", "delete_course(sess)"),
    Option("Delete section", "delete_section(sess)"),
    Option("List all departments", "list_departments(sess)"),
    Option("List all courses", "list_courses(sess)"),
    Option("List department courses", "list_department_courses(sess)"),
    Option("List course sections", "list_course_sections(sess)"),
    Option("Move course to new department", "move_course_to_new_department(sess)"),
    Option("Commit", "sess.commit()"),
    Option("Break out into shell", "IPython.embed()"),
    Option("Back", "back"),
    Option("Exit", "pass")
])"""

add_menu = Menu('add', "Please indicate what you want to add:", [
    Option("Department", "add_department(sess)"),
    Option("Course", "add_course(sess)"),
    Option("Major", "add_major(sess)"),
    #Option("Enrollment", "add_enrollment(sess)"),
    Option("Student", "add_student(sess)"),
    Option("Student to Major", "add_student_major(sess)"),
    Option("Major to Student", "add_major_student(sess)"),
    Option("Back", "back"),
    Option("Exit", "pass")
])

delete_menu = Menu('delete', "Please indicate what you want to delete from:", [
    Option("Department", "delete_department(sess)"),
    Option("Course", "delete_course(sess)"),
    Option("Major", "delete_major(sess)"),
    Option("Student", "delete_student(sess)"),
    Option("Student to Major", "delete_student_major(sess)"),
    Option("Major to Student", "delete_major_student(sess)"),
    Option("Back", "back"),
    Option("Exit", "pass")
])

list_menu = Menu('list', "Please indicate what you want to list:", [
    Option("Department", "list_department(sess)"),
    Option("Course", "list_course(sess)"),
    Option("Major", "list_major(sess)"),
    Option("Student", "list_student(sess)"),
    #Option("List Enrollments", "list_enrollment(sess)"),
    Option("Student to Major", "list_student_major(sess)"),
    Option("Major to Student", "list_major_student(sess)"),
    Option("Back", "back"),
    Option("Exit", "pass")
])

enrollment_menu = Menu('enrollment menu', "Please indicate what you want to do:", [
    Option("Add Enrollment", "add_enrollment(sess)"),
    Option("List Enrollments", "list_enrollment(sess)"),
    Option("Back", "back"),
    Option("Exit", "pass")
])

# A menu to prompt for the amount of logging information to go to the console.
debug_select = Menu('debug select', "Please select a debug level:", [
    Option("Informational", "logging.INFO"),
    Option("Debug", "logging.DEBUG"),
    Option("Error", "logging.ERROR")
])

# A menu to prompt for whether to create new tables or reuse the old ones.
introspection_select = Menu("introspection select", 'To introspect or not:', [
    Option('Start all over', START_OVER),
#   Option("Reuse tables", INTROSPECT_TABLES),
    Option("Reuse without introspection", REUSE_NO_INTROSPECTION)
])

other_options = Menu('Other options', "Please select one of the following options:", [
    Option("Boilerplate Data", "boilerplate(sess)"),
    Option("Commit", "sess.commit()"),
    Option("Rollback", "session_rollback(sess)"),
    Option("Exit this application", "pass"),
    Option("Back", "back")
])

menu_main = Menu('main', "Please select one of the following options:", [
    Option("Add", add_menu),
    Option("List", list_menu),
    Option("Delete", delete_menu),
    Option("Enrollment", enrollment_menu),
    Option("Other Options", other_options)
])




