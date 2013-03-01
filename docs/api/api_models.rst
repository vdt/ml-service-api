===================================
API Models
===================================

Organization
-----------------

An organization defines a group of users.  This can be a school, university, set of friends, etc.  Each organization
contains multiple courses, and multiple users.

User
-----------------

A user is the basic unit of the application.  Each user will belong to zero to many organizations, and will be a part of
zero to many courses.  Each user also will be associated with any essays that they have written, and any essay grades
that they have done.

Course
-----------------

The course is essentially a container for problems.  Each course can belong to zero to many organizations.  Each course
has zero to many users, and zero to many problems.

Problem
-----------------

A problem contains meta-information for a problem, such as a prompt, maximum scores, etc.  It contains zero to many essays,
and is a part of zero to many courses.

Essay
-----------------

The essay is the basic unit of written work.  Each essay is associated with a single problem and a single user.  It can have
multiple essay grades.

EssayGrade
-----------------

This is the basic unit that represents a single grader grading an essay.  Graders can be of multiple types (human,
machine, etc), and can give varying scores and feedback.  Each essaygrade is associated with a single user (if
human graded), and a single essay.

Membership
-----------------

This links between an organization and a user.  It has a field to indicate the role of the user within the organization.
Currently the roles are "student", "teacher", and "administrator."  The first user who creates an organization will
automatically be made an administrator.
