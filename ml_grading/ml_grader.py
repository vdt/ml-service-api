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

from freeform_data.models import Problem, Essay, EssayGrade

from ml_grading.models import CreatedModel

from ml_grading import ml_grading_util

sys.path.append(settings.ML_PATH)
import grade

from staff_grading import staff_grading_util

log = logging.getLogger(__name__)

RESULT_FAILURE_DICT={'success' : False, 'errors' : 'Errors!', 'confidence' : 0, 'feedback' : "", 'score' : 0}

def handle_single_item(essay):
    transaction.commit_unless_managed()
    success, latest_created_model = ml_grading_util.get_latest_created_model(essay.problem)
    if not success:
        log.error("No model exists yet for problem {0}".format(essay.problem))
        return False

    #strip out unicode and other characters in student response
    #Needed, or grader may potentially fail
    #TODO: Handle unicode in student responses properly
    student_response = essay.essay_text.encode('ascii', 'ignore')

    target_max_scores = json.loads(essay.problem.max_target_scores)
    target_counts = len(target_max_scores)

    for m in xrange(0,target_count):
        success, created_model=ml_grading_util.get_latest_created_model(sub.location)

        if not success:
            log.debug("Could not identify a valid created model!")
            if m==0:
                results= RESULT_FAILURE_DICT
                formatted_feedback="error"
                status=GraderStatus.failure
                statsd.increment("open_ended_assessment.grading_controller.call_ml_grader",
                    tags=["success:False"])

        else:

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

            log.debug("ML Grader:  Success: {0} Errors: {1}".format(results['success'], results['errors']))
            statsd.increment("open_ended_assessment.grading_controller.call_ml_grader",
                tags=["success:{0}".format(results['success']), 'location:{0}'.format(sub.location)])

            #Set grader status according to success/fail
            if results['success']:
                status = GraderStatus.success
            else:
                status = GraderStatus.failure

        if m==0:
            final_results=results
        elif results['success']==False:
            rubric_scores_complete = False
        else:
            rubric_scores.append(int(results['score']))
    if len(rubric_scores)==0:
        rubric_scores_complete=False

    grader_dict = {
        'score': int(final_results['score']),
        'feedback': json.dumps(results['feedback']),
        'status': status,
        'grader_id': 1,
        'grader_type': "ML",
        'confidence': results['confidence'],
        'submission_id': sub.id,
        'errors' : ' ' .join(results['errors']),
        'rubric_scores_complete' : rubric_scores_complete,
        'rubric_scores' : json.dumps(rubric_scores),
        }
    #Create grader object in controller by posting back results
    created, msg = util._http_post(
        controller_session,
        urlparse.urljoin(settings.GRADING_CONTROLLER_INTERFACE['url'],
            project_urls.ControllerURLs.put_result),
        grader_dict,
        settings.REQUESTS_TIMEOUT,
    )
    log.debug("Got response of {0} from server, message: {1}".format(created, msg))

    return sub_get_success

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


