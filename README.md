ML Service API
====================

Overview
---------------------
This is an API wrapper for a service to grade arbitrary free text responses.
This is licensed under the AGPL, please see LICENSE.txt for details.
The goal here is to provide a high-performance, scalable solution that can effectively help students learn.
Feedback is a major part of this process, the feedback system has been left very flexible on purpose (you will see this later on).

Note that you will need the machine-learning repository to use all of the functionality here.  This repo is currently internal to edX, but will
hopefully be open sourced shortly.  Until then, the API can be used, but the celery tasks will not work.

How to Contribute
-----------------------
Contributions are very welcome.  The easiest way is to fork this repo, and then make a pull request from your fork.

### Backlog as of 2/28

* Add in html serialization/deserialization for API views
* Add in permissions model
* Add way train "one-off" models for topicality, etc.
* Better tests (really, any tests)
* Documentation, particularly for installation
* A way to ensure that users belong to at least one organization
* Models to track activity across an organization
* Analytics views for api
* Add required/excluded fields to API resources
* Auth.json and env.json for deployment

Detailed Information
-------------------------
Please look in the docs folder for more detailed documentation.  There is a README there that explains how to build
and view the docs.

You can also see the latest documentation at [ReadtheDocs](http://ml-api.readthedocs.org/en/latest/) .