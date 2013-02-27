from celery import task
import logging
from celery.task import periodic_task
from freeform_data.models import Problem, Essay
from datetime import timedelta
from django.conf import settings
from ml_grading.ml_model_creation import handle_single_problem
from ml_grading.ml_grader import handle_single_essay
from django.db.models import Q

log=logging.getLogger(__name__)

@periodic_task(run_every=timedelta(seconds=settings.TIME_BETWEEN_ML_CREATOR_CHECKS))
def create_ml_models():
    problems = Problem.objects.all()
    for problem in problems:
        create_ml_models_single_problem(problem)

@task()
def create_ml_models_single_problem(problem):
    handle_single_problem(problem)

@periodic_task(run_every=timedelta(seconds=settings.TIME_BETWEEN_ML_GRADER_CHECKS))
def grade_ml():
    essays = Essay.objects.filter(has_been_ml_graded=False)
    for essay in essays:
        grade_ml_single_essay(essay)

@task()
def grade_ml_single_essay(essay):
    handle_single_essay(essay)