from tastypie.resources import ModelResource
from freeform_data.models import Organization, UserProfile, Course, Problem, Essay, EssayGrade
from django.contrib.auth.models import User
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication, ApiKeyAuthentication, BasicAuthentication, MultiAuthentication
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
    return MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())

def default_serialization():
    return Serializer(formats=['json', 'jsonp', 'xml', 'yaml', 'html', 'plist'])

class CreateUserResource(ModelResource):
    class Meta:
        allowed_methods = ['post']
        object_class = User
        authentication = Authentication()
        authorization = Authorization()
        fields = ['username']
        resource_name = "create_user"

    def obj_create(self, bundle, **kwargs):
        username, password = bundle.data['username'], bundle.data['password']
        try:
            bundle.obj = User.objects.create_user(username, '', password)
        except IntegrityError:
            raise BadRequest('That username already exists')
        return bundle

class OrganizationResource(ModelResource):
    class Meta:
        queryset = Organization.objects.all()
        resource_name = 'organization'

        serializer = default_serialization()
        authorization= default_authorization()
        authentication = default_authentication()

    def obj_create(self, bundle, **kwargs):
        return super(OrganizationResource, self).obj_create(bundle)

class UserProfileResource(ModelResource):
    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = 'user_profile'

        serializer = default_serialization()
        authorization= default_authorization()
        authentication = default_authentication()

    def obj_create(self, bundle, request=None, **kwargs):
        return super(UserProfileResource, self).obj_create(bundle,user=bundle.request.user)

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user_id=request.user.id)

class UserResource(ModelResource):
    essaygrades = fields.ToManyField('freeform_data.api.EssayGradeResource', 'essaygrade_set', null=True, related_name='user')
    essays = fields.ToManyField('freeform_data.api.EssayResource', 'essay_set', null=True, related_name='user')
    courses = fields.ToManyField('freeform_data.api.CourseResource', 'course_set', null=True)
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'

        serializer = default_serialization()
        authorization= default_authorization()
        authentication = default_authentication()

    def obj_create(self, bundle, **kwargs):
        return super(UserResource, self).obj_create(bundle)

    def dehydrate(self, bundle):
        bundle.data['api_key'] = bundle.obj.api_key.key
        return bundle

    def apply_authorization_limits(self, request, object_list):
        log.debug("Applying limits.")
        return object_list.filter(user_id=request.user.id)


class CourseResource(ModelResource):
    organization = fields.ForeignKey(OrganizationResource, 'organization', null=True)
    users = fields.ToManyField(UserResource, 'user_set', null=True)
    class Meta:
        queryset = Course.objects.all()
        resource_name = 'course'

        serializer = default_serialization()
        authorization= default_authorization()
        authentication = default_authentication()

    def obj_create(self, bundle, **kwargs):
        return super(CourseResource, self).obj_create(bundle, user=bundle.request.user)

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(organization=request.user.profile.organization)

class ProblemResource(ModelResource):
    essays = fields.ToManyField('freeform_data.api.EssayResource', 'essay_set', null=True, related_name='problem')
    courses = fields.ToManyField('freeform_data.api.CourseResource')
    class Meta:
        queryset = Problem.objects.all()
        resource_name = 'problem'

        serializer = default_serialization()
        authorization= default_authorization()
        authentication = default_authentication()

    def obj_create(self, bundle, **kwargs):
        return super(ProblemResource, self).obj_create(bundle)

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(course__in=request.user.profile.organization.course_set)

class EssayResource(ModelResource):
    essaygrades = fields.ToManyField('freeform_data.api.EssayGradeResource', 'essaygrade_set', null=True, related_name='essay')
    user = fields.ToOneField(UserResource, 'user')
    problem = fields.ToOneField(ProblemResource, 'problem')
    class Meta:
        queryset = Essay.objects.all()
        resource_name = 'essay'

        serializer = default_serialization()
        authorization= default_authorization()
        authentication = default_authentication()

    def obj_create(self, bundle, **kwargs):
        bundle = super(EssayGradeResource, self).obj_create(bundle, user=bundle.request.user)
        bundle.obj.user = request.user
        bundle.obj.save()

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user_id=request.user.id)

class EssayGradeResource(ModelResource):
    user = fields.ToOneField(UserResource, 'user', null=True)
    essay = fields.ToOneField(EssayResource, 'essay')
    class Meta:
        queryset = EssayGrade.objects.all()
        resource_name = 'essay_grade'

        serializer = default_serialization()
        authorization= default_authorization()
        authentication = default_authentication()

    def obj_create(self, bundle, **kwargs):
        bundle = super(EssayGradeResource, self).obj_create(bundle, user=bundle.request.user)
        bundle.obj.user = request.user
        bundle.obj.save()
        return bundle

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(essay__user_id=Q(request.user.id)|Q(user_id=request.user.id))