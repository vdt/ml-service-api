from tastypie.resources import ModelResource
from freeform_data.models import Organization, UserProfile, Course, Problem, Essay, EssayGrade
from django.contrib.auth.models import User
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication, ApiKeyAuthentication
from tastypie import fields
from django.conf.urls import url
from tastypie.utils import trailing_slash
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from tastypie.http import HttpGone, HttpMultipleChoices
from django.db.models import Q


class OrganizationResource(ModelResource):
    class Meta:
        queryset = Organization.objects.all()
        resource_name = 'organization'

        authorization= Authorization()
        authentication = ApiKeyAuthentication()

        def obj_create(self, bundle, request=None, **kwargs):
            return super(OrganizationResource, self).obj_create(bundle, request, user=request.user)

class UserProfileResource(ModelResource):
    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = 'user_profile'

        authorization= Authorization()
        authentication = ApiKeyAuthentication()

        def obj_create(self, bundle, request=None, **kwargs):
            return super(UserProfileResource, self).obj_create(bundle, request, user=request.user)

        def apply_authorization_limits(self, request, object_list):
            return object_list.filter(user_id=request.user.id)

class CourseResource(ModelResource):
    class Meta:
        queryset = Course.objects.all()
        resource_name = 'course'

        authorization= Authorization()
        authentication = ApiKeyAuthentication()

        def obj_create(self, bundle, request=None, **kwargs):
            return super(CourseResource, self).obj_create(bundle, request, user=request.user)

        def apply_authorization_limits(self, request, object_list):
            return object_list.filter(organization=request.user.profile.organization)

class ProblemResource(ModelResource):
    essays = fields.OneToManyField('freeform_data.api.EssayResource', 'essays', full=True, null=True)
    class Meta:
        queryset = Problem.objects.all()
        resource_name = 'problem'

        authorization= Authorization()
        authentication = ApiKeyAuthentication()

        def obj_create(self, bundle, request=None, **kwargs):
            return super(ProblemResource, self).obj_create(bundle, request, user=request.user)

        def apply_authorization_limits(self, request, object_list):
            return object_list.filter(course__in=request.user.profile.organization.course_set)

class EssayResource(ModelResource):
    essay_grades = fields.OneToManyField('freeform_data.api.EssayGradeResource', 'essay_grades', full=True, null=True)
    user = fields.ForeignKey(UserProfileResource, 'user')
    class Meta:
        queryset = Essay.objects.all()
        resource_name = 'essay'

        authorization= Authorization()
        authentication = ApiKeyAuthentication()

        def obj_create(self, bundle, request=None, **kwargs):
            return super(EssayResource, self).obj_create(bundle, request, user=request.user)

        def apply_authorization_limits(self, request, object_list):
            return object_list.filter(user_id=request.user.id)

class EssayGradeResource(ModelResource):
    user = fields.ForeignKey(UserProfileResource, 'user', null=True)
    class Meta:
        queryset = EssayGrade.objects.all()
        resource_name = 'essay_grade'

        authorization= Authorization()
        authentication = ApiKeyAuthentication()

        def obj_create(self, bundle, request=None, **kwargs):
            return super(EssayGradeResource, self).obj_create(bundle, request, user=request.user)

        def apply_authorization_limits(self, request, object_list):
            return object_list.filter(essay__user_id=Q(request.user.id)|Q(user_id=request.user.id))