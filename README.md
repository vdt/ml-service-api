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

1. apt-get install git python'
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
