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
import json
from ConfigParser import SafeConfigParser
from datetime import datetime

from freeform_data.models import Organization, Course, UserProfile, Problem, Essay, EssayGrade
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

        header_name = "importdata"

        prompt = parser.get(header_name, 'prompt')
        essay_file = parser.get(header_name, 'essay_file')
        essay_limit = int(parser.get(header_name, 'essay_limit'))
        name = parser.get(header_name, "name")
        add_score = parser.get(header_name, "add_grader_object") == "True"
        max_target_scores = json.loads(parser.get(header_name, "max_target_scores"))
        grader_type = parser.get(header_name, "grader_type")

        try:
            User.objects.create_user('vik', 'vik@edx.org', 'vik')
        except:
            #User already exists, but doesn't matter to us
            pass

        user = User.objects.get(username='vik')
        organization, created = Organization.objects.get_or_create(
            organization_name = "edX"
        )

        course, created = Course.objects.get_or_create(
            course_name = "edX101",
            organization = organization
        )

        user.profile.organization = organization
        user.save()
        course.users.add(user.profile)
        course.save()

        problem, created = Problem.objects.get_or_create(
            prompt = prompt,
            name = name,
        )
        problem.courses.add(course)
        problem.save()

        grades, text = [], []
        log.debug(settings.REPO_PATH)
        combined_raw = open(settings.REPO_PATH / essay_file).read()
        raw_lines = combined_raw.splitlines()
        for row in xrange(1, len(raw_lines)):
            line_split = raw_lines[row].strip().split("\t")
            text.append(line_split[0])
            grades.append(line_split[1:])

        for i in range(0, min(essay_limit, len(text))):
            essay = Essay(
                problem = problem,
                user =user.profile,
                essay_type = "train",
                essay_text = text[i],
            )

            essay.save()
            score = EssayGrade(
                target_scores=json.dumps(grades[i]),
                feedback="",
                grader_type = grader_type,
                essay = essay,
                success = True,
            )
            score.save()

        print ("Successfully imported {0} essays using configuration in file {1}.".format(
            min(essay_limit, len(text)),
            args[0],
        ))