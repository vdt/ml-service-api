"""
Used by celery to decide what tasks it needs to do
"""

from celery import task
import logging
from celery.task import periodic_task
from freeform_data.models import Problem, Essay
from datetime import timedelta
from django.conf import settings
from ml_grading.ml_model_creation import handle_single_problem, MIN_ESSAYS_TO_TRAIN_WITH
from ml_grading.ml_grader import handle_single_essay
from django.db.models import Q, Count
from django.db import transaction

log=logging.getLogger(__name__)

@periodic_task(run_every=timedelta(seconds=settings.TIME_BETWEEN_ML_CREATOR_CHECKS))
def create_ml_models():
    """
    Called periodically by celery.  Loops through each problem and tries to create a model for it.
    """
    transaction.commit_unless_managed()
    problems = Problem.objects.all()
    for problem in problems:
        create_ml_models_single_problem(problem)

@task()
def create_ml_models_single_problem(problem):
    """
    Celery task called by create_ml_models to create a single model
    """
    transaction.commit_unless_managed()
    handle_single_problem(problem)

@periodic_task(run_every=timedelta(seconds=settings.TIME_BETWEEN_ML_GRADER_CHECKS))
def grade_ml():
    """
    Called periodically by celery.  Loops through each problem, sees if there are enough essays for ML grading to work,
    and then calls the ml grader if there are.
    """
    transaction.commit_unless_managed()
    #TODO: Add in some checking to ensure that count is of instructor graded essays only
    problems = Problem.objects.all().annotate(essay_count=Count('essay')).filter(essay_count__gt=(MIN_ESSAYS_TO_TRAIN_WITH-1))
    essays = Essay.objects.filter(problem__in=problems, has_been_ml_graded=False)
    for essay in essays:
        grade_ml_single_essay(essay)

@task()
def grade_ml_single_essay(essay):
    """
    Called by grade_ml.  Handles a single grading task for a single essay.
    """
    transaction.commit_unless_managed()
    handle_single_essay(essay)