from django.conf import settings
from django.core.management.base import NoArgsCommand
from django.utils import timezone
from django.db import transaction
import urlparse
import time
import json
import logging
import sys
from statsd import statsd
import pickle
from ml_grading.models import CreatedModel
from ml_grading import ml_grading_util

sys.path.append(settings.ML_PATH)
import create

log = logging.getLogger(__name__)

MAX_ESSAYS_TO_TRAIN_WITH = 1000
MIN_ESSAYS_TO_TRAIN_WITH = 10

def handle_single_problem(problem):
    transaction.commit_unless_managed()
    prompt = problem.prompt
    essays = problem.essay_set.filter(essay_type="train")
    essay_text = []
    essay_grades = []
    essay_text_vals = essays.values('essay_text')
    for i in xrange(0,len(essays)):
        try:
            essay_grades.append(json.loads(essays[i].get_instructor_scored()[0].target_scores))
            essay_text.append(essay_text_vals[i]['essay_text'])
        except:
            log.exception("Could not get latest instructor scored for {0}".format(essays[i]))
    log.debug(essay_grades)

    try:
        essay_text = [et.encode('ascii', 'ignore') for et in essay_text]
    except:
        error_message = "Could not correctly encode some submissions: {0}".format(essay_text)
        log.exception(error_message)
        return False, error_message

    first_len = len(json.loads(problem.max_target_scores))
    for i in xrange(0,len(essay_grades)):
        if len(essay_grades[i])!=first_len:
            error_message = "Problem with an instructor scored essay! {0}".format(essay_grades)
            log.exception(error_message)
            return False, error_message

    if len(essay_text)>MAX_ESSAYS_TO_TRAIN_WITH:
        essay_text = essay_text[:MAX_ESSAYS_TO_TRAIN_WITH]
        essay_grades = essay_grades[:MAX_ESSAYS_TO_TRAIN_WITH]

    graded_sub_count = len(essay_text)
    if graded_sub_count < MIN_ESSAYS_TO_TRAIN_WITH:
        error_message = "Too few too create a model for problem {0}".format(problem)
        log.error(error_message)
        return False, error_message

    for m in xrange(0,first_len):
        scores = [s[m] for s in essay_grades]
        max_score = max(scores)
        log.debug("Currently on location {0} in problem {1}".format(m, problem.id))
        #Get paths to ml model from database
        relative_model_path, full_model_path= ml_grading_util.get_model_path(problem,m)
        #Get last created model for given location
        transaction.commit_unless_managed()
        success, latest_created_model=ml_grading_util.get_latest_created_model(problem,m)

        if success:
            sub_count_diff=graded_sub_count-latest_created_model.number_of_essays
        else:
            sub_count_diff = graded_sub_count

        #Retrain if no model exists, or every 10 graded essays.
        if not success or sub_count_diff>=10:
            #Checks to see if another model creator process has started amodel for this location
            success, model_started, created_model = ml_grading_util.check_if_model_started(problem)

            #Checks to see if model was started a long time ago, and removes and retries if it was.
            if model_started:
                now = timezone.now()
                second_difference = (now - created_model.modified).total_seconds()
                if second_difference > settings.TIME_BEFORE_REMOVING_STARTED_MODEL:
                    log.error("Model for problem {0} started over {1} seconds ago, removing and re-attempting.".format(
                        problem_id, settings.TIME_BEFORE_REMOVING_STARTED_MODEL))
                    created_model.delete()
                    model_started = False

            if not model_started:
                created_model_dict_initial={
                    'max_score' : max_score,
                    'prompt' : prompt,
                    'problem' : problem,
                    'model_relative_path' : relative_model_path,
                    'model_full_path' : full_model_path,
                    'number_of_essays' : graded_sub_count,
                    'creation_succeeded': False,
                    'creation_started' : True,
                    'target_number' : m,
                    }
                created_model = CreatedModel(**created_model_dict_initial)
                created_model.save()
                transaction.commit_unless_managed()

                if not isinstance(prompt, basestring):
                    try:
                        prompt = str(prompt)
                    except:
                        prompt = ""
                prompt = prompt.encode('ascii', 'ignore')

                results = create.create(essay_text, scores, prompt)

                scores = [int(score_item) for score_item in scores]
                #Add in needed stuff that ml creator does not pass back
                results.update({
                    'model_path' : full_model_path,
                    'relative_model_path' : relative_model_path
                })

                #Try to create model if ml model creator was successful
                if results['success']:
                    try:
                        success, s3_public_url = save_model_file(results,settings.USE_S3_TO_STORE_MODELS)
                        results.update({'s3_public_url' : s3_public_url, 'success' : success})
                        if not success:
                            results['errors'].append("Could not save model.")
                    except:
                        results['errors'].append("Could not save model.")
                        results['s3_public_url'] = ""
                        log.exception("Problem saving ML model.")

                created_model_dict_final={
                    'cv_kappa' : results['cv_kappa'],
                    'cv_mean_absolute_error' : results['cv_mean_absolute_error'],
                    'creation_succeeded': results['success'],
                    'creation_started' : False,
                    's3_public_url' : results['s3_public_url'],
                    'model_stored_in_s3' : settings.USE_S3_TO_STORE_MODELS,
                    's3_bucketname' : str(settings.S3_BUCKETNAME),
                    'model_relative_path' : relative_model_path,
                    'model_full_path' : full_model_path,
                    }

                transaction.commit_unless_managed()
                try:
                    CreatedModel.objects.filter(pk=created_model.pk).update(**created_model_dict_final)
                except:
                    log.error("ModelCreator creation failed.  Error: {0}".format(id))

                log.debug("Location: {0} Creation Status: {1} Errors: {2}".format(
                    full_model_path,
                    results['success'],
                    results['errors'],
                ))
    transaction.commit_unless_managed()
    return True, "Creation succeeded."

def save_model_file(results, save_to_s3):
    success=False
    if save_to_s3:
        pickled_model=ml_grading_util.get_pickle_data(results['prompt'], results['feature_ext'],
            results['classifier'], results['text'],
            results['score'])
        success, s3_public_url=ml_grading_util.upload_to_s3(pickled_model, results['relative_model_path'], str(settings.S3_BUCKETNAME))

    try:
        ml_grading_util.dump_model_to_file(results['prompt'], results['feature_ext'],
            results['classifier'], results['text'],results['score'],results['model_path'])
        if success:
            return True, s3_public_url
        else:
            return True, "Saved model to file."
    except:
        return False, "Could not save model."