==================================
Usage
==================================

You will need to run both the API server, and the celery backend to process tasks.

1. python manage.py runserver 127.0.0.1:9000
2. python manage.py celeryd -B --settings=ml_service_api.settings --pythonpath=DIR WHERE YOU CLONED REPO  --loglevel=debug

Frontend Usage
------------------------------
There is an easy to use frontend.  In order to use it, just navigate to 127.0.0.1:9000.  After that, you will be able to register using the links at the top.  After you register, you will see links to the API models.  Each model will allow you to get a list of existing models, add new ones, delete existing ones, and update them.  See the :ref:`api_models` section for more details on the models.

API Usage
------------------------------
You will able to interact with the API by going to http://127.0.0.1:9000/essay_site/api/v1/?format=json .
This will show you all of the API endpoints.

In order to begin, you will first have to create a user.
You can use http://127.0.0.1:9000/essay_site/api/v1/createuser/ to do this.
Just POST a JSON data dictionary containing the keys username and password (ie {"username" : "user", "password" : "pass"}
The postman add-on for Chrome is highly recommended to do this.

Once you create a user, you will be able to interact with the various API resources.  I will get into how they
are organized below.