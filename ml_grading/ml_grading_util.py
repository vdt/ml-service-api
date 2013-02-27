import os
from path import path
from django.conf import settings
import re
from django.utils import timezone
from django.db import transaction
import pickle
import logging

from models import CreatedModel

from boto.s3.connection import S3Connection
from boto.s3.key import Key

import controller.rubric_functions
from controller.models import Submission, SubmissionState, Grader
log=logging.getLogger(__name__)

def create_directory(model_path):
    directory=path(model_path).dirname()
    if not os.path.exists(directory):
        os.makedirs(directory)

    return True

def get_model_path(problem, suffix=0):
    """
    Generate a path from a location
    """
    problem_id = problem.id

    base_path=settings.ML_MODEL_PATH
    #Ensure that directory exists, create if it doesn't
    create_directory(base_path)

    fixed_location="{0}_{1}".format(problem_id,suffix)
    fixed_location+="_"+timezone.now().strftime("%Y%m%d%H%M%S")
    full_path=os.path.join(base_path,fixed_location)
    return fixed_location,full_path


def get_latest_created_model(problem):
    """
    Gets the current model file for a given location
    Input:
        location
    Output:
        Boolean success/fail, createdmodel object/error message
    """
    created_models=CreatedModel.objects.filter(
        problem=problem,
        creation_succeeded=True,
        creation_finished = True,
    ).order_by("-date_created")[:1]

    if created_models.count()==0:
        return False, "No valid models for location."

    return True, created_models[0]


def check_if_model_started(problem):
    """
    Gets the currently active model file for a given location
    Input:
        location
    Output:
        Boolean success/fail, Boolean started/not started
    """
    model_started = False
    created_models=CreatedModel.objects.filter(
        problem=problem,
        creation_started=True
    ).order_by("-date_created")[:1]

    if created_models.count()==0:
        return True, model_started, ""

    created_model = created_models[0]
    if created_model.creation_succeeded==False:
        model_started = True

    return True, model_started, created_model