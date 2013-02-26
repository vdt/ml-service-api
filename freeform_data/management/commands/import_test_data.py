from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone

#from http://jamesmckay.net/2009/03/django-custom-managepy-commands-not-committing-transactions/
#Fix issue where db data in manage.py commands is not refreshed at all once they start running
from django.db import transaction
transaction.commit_unless_managed()

import requests
import urlparse
import time
import json
import logging
import sys
from ConfigParser import SafeConfigParser
from datetime import datetime

from essay_api.models import Essay, EssaySet, Score, ScoreStatus, EssayState
from django.contrib.auth.models import User

log = logging.getLogger(__name__)

class Command(BaseCommand):
    args = "<filename>"
    help = "Poll grading controller and send items to be graded to ml"


    def handle(self, *args, **options):
        """
        Read from file
        """

        parser = SafeConfigParser()
        parser.read(args[0])

        print("Starting import...")
        print("Reading config from file {0}".format(args[0]))

        user=User.objects.get(id=1)
        header_name = "importdata"

        prompt = parser.get(header_name, 'prompt')
        essay_file = parser.get(header_name, 'essay_file')
        essay_limit = int(parser.get(header_name, 'essay_limit'))
        state = parser.get(header_name, "state")
        add_score = parser.get(header_name, "add_score_object") == "True"
        max_score= int(parser.get(header_name,"max_score"))
        min_score = int(parser.get(header_name,"min_score"))
        essay_set_id = int(parser.get(header_name,"essay_set_id"))
        essay_type = parser.get(header_name,"essay_type")

        try:
            essay_set = EssaySet.objects.get(id=essay_set_id)
        except:
            essay_set = EssaySet(
                prompt=prompt,
                max_score=max_score,
                min_score=min_score,
                user=user,
                customer_data = user.customerdata,
                grader_type = "CL",
                scale_type = "CO",
            )
            essay_set.save()

        grade, text = [], []
        log.debug(settings.REPO_PATH)
        combined_raw = open(settings.REPO_PATH / essay_file).read()
        raw_lines = combined_raw.splitlines()
        for row in xrange(1, len(raw_lines)):
            score1, text1 = raw_lines[row].strip().split("\t")
            text.append(text1)
            grade.append(int(score1))

        for i in range(0, min(essay_limit, len(text))):
            essay = Essay(
                essay_set = essay_set,
                user =user,
                type = essay_type,
                state = state,
                text = text[i],
            )

            essay.save()
            if add_score:
                score = Score(
                    grade=grade[i],
                    feedback="",
                    essay = essay,
                    status=ScoreStatus.success,
                    grader_id="",
                    confidence=1,
                )
                score.save()


        print ("Successfully imported {0} essays using configuration in file {1}.".format(
            min(essay_limit, len(text)),
            args[0],
        ))