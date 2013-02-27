from celery import task
import logging
from celery.task import periodic_task
from freeform_data.models import Problem
from datetime import timedelta
from django.conf import settings
from ml_grading.ml_model_creation import handle_single_location

log=logging.getLogger(__name__)

@periodic_task(run_every=timedelta(seconds=30))
def create_ml_models():
    problems = Problem.objects.all()
    for problem in problems:
        create_ml_models_single_problem(problem)

@task()
def create_ml_models_single_problem():
    handle_single_location(problem)
