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
    ).order_by("-date_created")[:1]

    if created_models.count()==0:
        return True, model_started, ""

    created_model = created_models[0]
    if created_model.creation_succeeded==False and created_model.creation_started==True:
        model_started = True

    return True, model_started, created_model

def upload_to_s3(string_to_upload, keyname, bucketname):
    '''
    Upload file to S3 using provided keyname.

    Returns:
        public_url: URL to access uploaded file
    '''
    try:
        conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        bucketname = str(bucketname)
        bucket = conn.create_bucket(bucketname.lower())

        k = Key(bucket)
        k.key = keyname
        k.set_contents_from_string(string_to_upload)
        public_url = k.generate_url(60*60*24*365) # URL timeout in seconds.

        return True, public_url
    except:
        return False, "Could not connect to S3."

def get_pickle_data(prompt_string, feature_ext, classifier, text, score):
    """
    Writes out a model to a file.
    prompt string is a string containing the prompt
    feature_ext is a trained FeatureExtractor object
    classifier is a trained classifier
    model_path is the path of write out the model file to
    """
    model_file = {'prompt': prompt_string, 'extractor': feature_ext, 'model': classifier, 'text' : text, 'score' : score}
    return pickle.dumps(model_file)

def dump_model_to_file(prompt_string, feature_ext, classifier, text, score,model_path):
    model_file = {'prompt': prompt_string, 'extractor': feature_ext, 'model': classifier, 'text' : text, 'score' : score}
    pickle.dump(model_file, file=open(model_path, "w"))