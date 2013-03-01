=================================================
API Structure
=================================================
The API is structured around Django models.  Tastypie abstracts the API into model resources.  These resources allow
for GET/POST/PUT/DELETE operations on the models.  This allows for a very simple interface.  You may have also noted
the ?format=json blocks earlier.  A variety of format can be used, including 'json', 'jsonp', 'xml', 'yaml', 'html', and 'plist'.
Note that HTML will return a "not implemented yet" message.

The available models are organization, userprofile, user, course, problem, essay, essaygrade.  Each model can be
accessed via http://127.0.0.1:9000/essay_site/api/v1/MODEL_NAME_HERE/ Appending schema to the end of this will
show you the available actions.

By default, each user is restricted to only seeing the objects that they created.  This will be changed a bit when
a permissions model is added.