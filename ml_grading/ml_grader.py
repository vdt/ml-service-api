from django.conf import settings
from django.db import transaction
from django.utils import timezone
import requests
import urlparse
import time
import json
import logging
import sys
import os
from path import path
from statsd import statsd
import pickle

log=logging.getLogger(__name__)

from freeform_data.models import Problem, Essay, EssayGrade, GraderTypes

from ml_grading.models import CreatedModel

from ml_grading import ml_grading_util

sys.path.append(settings.ML_PATH)
import grade

log = logging.getLogger(__name__)

RESULT_FAILURE_DICT={'success' : False, 'errors' : 'Errors!', 'confidence' : 0, 'feedback' : "", 'score' : 0}

def handle_single_essay(essay):
    transaction.commit_unless_managed()

    #strip out unicode and other characters in student response
    #Needed, or grader may potentially fail
    #TODO: Handle unicode in student responses properly
    student_response = essay.essay_text.encode('ascii', 'ignore')

    target_max_scores = json.loads(essay.problem.max_target_scores)
    target_counts = len(target_max_scores)

    target_scores=[]
    for m in xrange(0,target_counts):
        success, created_model=ml_grading_util.get_latest_created_model(essay.problem,m)

        if not success:
            error_message = "Could not identify a valid created model!"
            log.error(error_message)
            results= RESULT_FAILURE_DICT
            formatted_feedback="error"
            return False, error_message

        #Create grader path from location in submission
        grader_path = os.path.join(settings.ML_MODEL_PATH,created_model.model_relative_path)
        model_stored_in_s3=created_model.model_stored_in_s3

        success, grader_data=load_model_file(created_model,use_full_path=False)
        if success:
            results = grade.grade(grader_data, student_response)
        else:
            results=RESULT_FAILURE_DICT

        #If the above fails, try using the full path in the created_model object
        if not results['success'] and not created_model.model_stored_in_s3:
            grader_path=created_model.model_full_path
            try:
                success, grader_data=load_model_file(created_model,use_full_path=True)
                if success:
                    results = grade.grade(grader_data, student_response)
                else:
                    results=RESULT_FAILURE_DICT
            except:
                error_message="Could not find a valid model file."
                log.exception(error_message)
                results=RESULT_FAILURE_DICT

        if m==0:
            final_results=results
        if results['success'] == False:
            final_results['success'] = False
        target_scores.append(int(results['score']))

    grader_dict = {
        'essay' : essay,
        'target_scores' : json.dumps(target_scores),
        'grader_type' : GraderTypes.machine,
        'feedback' : '',
        'annotated_text' : '',
        'premium_feedback_scores' : json.dumps([]),
        'success' :final_results['success'],
        'confidence' : final_results['confidence'],
        }
    #Create grader object in controller by posting back results
    essay_grade = EssayGrade(**grader_dict)
    essay_grade.save()

    essay.has_been_ml_graded = True
    essay.save()

    return True, "Successfully scored!"

def load_model_file(created_model,use_full_path):
    try:
        if use_full_path:
            grader_data=pickle.load(file(created_model.model_full_path,"r"))
        else:
            grader_data=pickle.load(file(os.path.join(settings.ML_MODEL_PATH,created_model.model_relative_path),"r"))
        return True, grader_data
    except:
        log.exception("Could not load model file.  This is okay.")
        #Move on to trying S3
        pass

    try:
        r = requests.get(created_model.s3_public_url, timeout=2)
        grader_data=pickle.loads(r.text)
    except:
        log.exception("Problem with S3 connection.")
        return False, "Could not load."

    try:
        store_model_locally(created_model,grader_data)
    except:
        log.exception("Could not save model.  This is not a show-stopping error.")
        #This is okay if it isn't possible to save locally
        pass

    return True, grader_data

def store_model_locally(created_model,results):
    relative_model_path= created_model.model_relative_path
    full_model_path = os.path.join(settings.ML_MODEL_PATH,relative_model_path)
    try:
        ml_grading_util.dump_model_to_file(results['prompt'], results['extractor'],
            results['model'], results['text'],results['score'],full_model_path)
    except:
        error_message="Could not save model to file."
        log.exception(error_message)
        return False, error_message

    return True, "Saved file."


