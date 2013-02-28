ML Service API
====================

Overview
---------------------
This is an API wrapper for a service to grade arbitrary free text responses.
This is licensed under the AGPL, please see LICENSE.txt for details.
The goal here is to provide a high-performance, scalable solution that can effectively help students learn.
Feedback is a major part of this process, the feedback system has been left very flexible on purpose (you will see this later on).

The key technologies that are utilized in this API wrapper are:
* Python
* Django
* Tastypie (Django api framework)
* Celery (For periodic tasks, ie ML grading and model creation)
* South (for database migrations)

Note that you will need the machine-learning repository to use all of the functionality here.  This repo is currently internal to edX, but will
hopefully be open sourced shortly.  Until then, the API can be used, but the celery tasks will not work.

Installation
----------------------
Please see install_notes.txt in the documentation directory for more detailed install information.
Looking at fabfile.py is also a good idea of how to install this.  The commands in fabfile will take a system
from a fresh start to a fully working install.
The main steps are:

1. apt-get install git python
2. git clone git@github.com:edx/ml-service-api.git
3. xargs -a apt-packages.txt apt-get install
4. apt-get install python-pip
5. pip install virtualenv
6. mkdir /opt/edx
7. virtualenv "/opt/edx"
8. source /opt/edx/bin/activate
9. pip install -r requirements.txt
10. python manage.py syncdb --settings=ml_service_api.settings --pythonpath=DIR WHERE YOU CLONED REPO
11. python manage.py migrate --settings=ml_service_api.settings --pythonpath=DIR WHERE YOU CLONED REPO

You can skip the virtualenv commands if you like, but they will be a major help in keeping the packages
for this repo separate from the rest of your system.

If you get errors using the above, you may need to create a database directory one level up from where you cloned
the git repo (folder named "db")

Usage
-----------------------
You will need to run both the API server, and the celery backend to process tasks.

1. python manage.py runserver 127.0.0.1:9000
2. python manage.py celeryd -B --settings=ml_service_api.settings --pythonpath=DIR WHERE YOU CLONED REPO  --loglevel=debug

After that, you will able to interact with the API by going to http://127.0.0.1:9000/essay_site/api/v1/?format=json .
This will show you all of the API endpoints.

In order to begin, you will first have to create a user.
You can use http://127.0.0.1:9000/essay_site/api/v1/createuser/ to do this.
Just POST a JSON data dictionary containing the keys username and password (ie {"username" : "user", "password" : "pass"}
The postman add-on for Chrome is highly recommended to do this.

Once you create a user, you will be able to interact with the various API resources.  I will get into how they
are organized below.

API Structure
-----------------------
The API is structured around Django models.  Tastypie abstracts the API into model resources.  These resources allow
for GET/POST/PUT/DELETE operations on the models.  This allows for a very simple interface.  You may have also noted
the ?format=json blocks earlier.  A variety of format can be used, including 'json', 'jsonp', 'xml', 'yaml', 'html', and 'plist'.
Note that HTML will return a "not implemented yet" message.

The available models are organization, userprofile, user, course, problem, essay, essaygrade.  Each model can be
accessed via http://127.0.0.1:9000/essay_site/api/v1/MODEL_NAME_HERE/ Appending schema to the end of this will
show you the available actions.

By default, each user is restricted to only seeing the objects that they created.  This will be changed a bit when
a permissions model is added.

API Models
-------------------------

### Organization

An organization defines a group of users.  This can be a school, university, set of friends, etc.  Each organization
contains multiple courses, and multiple users.

### User

A user is the basic unit of the application.  Each user will belong to zero to many organizations, and will be a part of
zero to many courses.  Each user also will be associated with any essays that they have written, and any essay grades
that they have done.

### Course

The course is essentially a container for problems.  Each course can belong to zero to many organizations.  Each course
has zero to many users, and zero to many problems.

### Problem

A problem contains meta-information for a problem, such as a prompt, maximum scores, etc.  It contains zero to many essays,
and is a part of zero to many courses.

### Essay

The essay is the basic unit of written work.  Each essay is associated with a single problem and a single user.  It can have
multiple essay grades.

### EssayGrade

This is the basic unit that represents a single grader grading an essay.  Graders can be of multiple types (human,
machine, etc), and can give varying scores and feedback.  Each essaygrade is associated with a single user (if
human graded), and a single essay.

