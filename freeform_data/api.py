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
from tastypie.serializers import Serializer
from django.db import IntegrityError
from tastypie.exceptions import BadRequest
import logging
log=logging.getLogger(__name__)

def default_authorization():
    return Authorization()

def default_authentication():
    return ApiKeyAuthentication()

def default_serialization():
    return Serializer(formats=['json', 'jsonp', 'xml', 'yaml', 'html', 'plist'])

class CreateUserResource(ModelResource):
    class Meta:
        allowed_methods = ['post']
        object_class = User
        authentication = Authentication()
        authorization = Authorization()
        include_resource_uri = False
        fields = ['username']
        resource_name = 'create_user'

    def obj_create(self, bundle, request=None, **kwargs):
        try:
            bundle.request = request
            bundle = super(CreateUserResource, self).obj_create(bundle, **kwargs)
            bundle.obj.set_password(bundle.data.get('password'))
            bundle.obj.save()
        except IntegrityError:
            log.exception("Could not create the user.")
            raise BadRequest('That username already exists')
        return bundle

class OrganizationResource(ModelResource):
    class Meta:
        queryset = Organization.objects.all()
        resource_name = 'organization'

        serializer = default_serialization()
        authorization= default_authorization()
        authentication = default_authentication()

        def obj_create(self, bundle, request=None, **kwargs):
            bundle.request = request
            return super(OrganizationResource, self).obj_create(bundle)

class UserProfileResource(ModelResource):
    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = 'user_profile'

        serializer = default_serialization()
        authorization= default_authorization()
        authentication = default_authentication()

        def obj_create(self, bundle, request=None, **kwargs):
            bundle.request = request
            return super(UserProfileResource, self).obj_create(bundle,user=request.user)

        def apply_authorization_limits(self, request, object_list):
            return object_list.filter(user_id=request.user.id)

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'

        serializer = default_serialization()
        authorization= default_authorization()
        authentication = default_authentication()

        def obj_create(self, bundle, request=None, **kwargs):
            bundle.request = request
            return super(UserProfileResource, self).obj_create(bundle)

        def apply_authorization_limits(self, request, object_list):
            return object_list.filter(user_id=request.user.id)

class CourseResource(ModelResource):
    class Meta:
        queryset = Course.objects.all()
        resource_name = 'course'

        serializer = default_serialization()
        authorization= default_authorization()
        authentication = default_authentication()

        def obj_create(self, bundle, request=None, **kwargs):
            bundle.request = request
            return super(CourseResource, self).obj_create(bundle, user=request.user)

        def apply_authorization_limits(self, request, object_list):
            return object_list.filter(organization=request.user.profile.organization)

class ProblemResource(ModelResource):
    essays = fields.OneToManyField('freeform_data.api.EssayResource', 'essay_set', full=True, null=True)
    class Meta:
        queryset = Problem.objects.all()
        resource_name = 'problem'

        serializer = default_serialization()
        authorization= default_authorization()
        authentication = default_authentication()

        def obj_create(self, bundle, request=None, **kwargs):
            bundle.request = request
            return super(ProblemResource, self).obj_create(bundle)

        def apply_authorization_limits(self, request, object_list):
            return object_list.filter(course__in=request.user.profile.organization.course_set)

class EssayResource(ModelResource):
    essay_grades = fields.OneToManyField('freeform_data.api.EssayGradeResource', 'essaygrade_set', full=True, null=True)
    user = fields.ForeignKey(UserResource, 'user', null=True)
    problem = fields.ForeignKey(ProblemResource, 'problem')
    class Meta:
        queryset = Essay.objects.all()
        resource_name = 'essay'

        serializer = default_serialization()
        authorization= default_authorization()
        authentication = default_authentication()

        def obj_create(self, bundle, request=None, **kwargs):
            bundle.request = request
            bundle = super(EssayGradeResource, self).obj_create(bundle, user=request.user)
            bundle.obj.user = request.user
            bundle.obj.save()

        def apply_authorization_limits(self, request, object_list):
            return object_list.filter(user_id=request.user.id)

class EssayGradeResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user', null=True)
    class Meta:
        queryset = EssayGrade.objects.all()
        resource_name = 'essay_grade'

        serializer = default_serialization()
        authorization= default_authorization()
        authentication = default_authentication()

        def obj_create(self, bundle, request=None, **kwargs):
            bundle.request = request
            bundle = super(EssayGradeResource, self).obj_create(bundle, user=request.user)
            bundle.obj.user = request.user
            bundle.obj.save()
            return bundle

        def apply_authorization_limits(self, request, object_list):
            return object_list.filter(essay__user_id=Q(request.user.id)|Q(user_id=request.user.id))