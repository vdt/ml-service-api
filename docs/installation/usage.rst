==================================
Usage
==================================
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