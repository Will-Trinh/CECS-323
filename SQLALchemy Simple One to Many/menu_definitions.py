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


# The menu options for operating on Departments.
course_main = Menu('Department', 'Department Options:', [
    Option("Add department", "add_department(sess)"),
    Option("Delete department", "delete_department(sess)"),
    Option("Select Department", "find_department(sess)"),
    Option("List department courses", "list_department_courses(sess)"),
    Option("List all departments", "list_department(sess)"),
    Option("Commit", "sess.commit()"),
    Option("Break out into shell", "IPython.embed()"),
    Option("Exit", "pass")
])

department_select = Menu('Department select', "Please select how you want to select a department:", [
    Option("Abbreviation", "abbreviation"),
    Option("Chair Name", "chair"),
    Option("Building and Office", "building/office"),
    Option("Description", "description")
])

# The menu options for operating on Courses.
course_main = Menu('Course', 'Course Options:', [
    Option("Add course", "add_course(sess)"),
    Option("Delete course", "delete_course(sess)"),
    Option("List all courses", "list_courses(sess)"),
    Option("Move course to new department", "move_course_to_new_department(sess)"),
    Option("Commit", "sess.commit()"),
    Option("Break out into shell", "IPython.embed()"),
    Option("Exit", "pass")
])

# A menu to prompt for the amount of logging information to go to the console.
debug_select = Menu('debug select', 'Please select a debug level:', [
    Option("Informational", "logging.INFO"),
    Option("Debug", "logging.DEBUG"),
    Option("Error", "logging.ERROR")
])

# A menu to prompt for whether to create new tables or reuse the old ones.
introspection_select = Menu("introspection selectt", 'To introspect or not:', [
    Option('Start all over', START_OVER),
    Option("Reuse tables", INTROSPECT_TABLES),
    Option("Reuse without introspection", REUSE_NO_INTROSPECTION)
])
