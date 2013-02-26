from tastypie.resources import ModelResource
from freeform_data.models import Organization, UserProfile, Course, Problem, Essay, EssayGrade
from django.contrib.auth import User


class OrganizationResource(ModelResource):
    class Meta:
        queryset = Organization.objects.all()
        resource_name = 'organization'

class UserProfileResource(ModelResource):
    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = 'user_profile'

class CourseResource(ModelResource):
    class Meta:
        queryset = Course.objects.all()
        resource_name = 'course'

class ProblemResource(ModelResource):
    class Meta:
        queryset = Problem.objects.all()
        resource_name = 'problem'

class EssayResource(ModelResource):
    class Meta:
        queryset = Essay.objects.all()
        resource_name = 'essay'

class EssayGradeResource(ModelResource):
    class Meta:
        queryset = EssayGrade.objects.all()
        resource_name = 'essay_grade'