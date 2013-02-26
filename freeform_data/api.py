from tastypie.resources import ModelResource
from freeform_data.models import Organization, UserProfile, Course, Problem, Essay, EssayGrade
from django.contrib.auth import User
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication, ApiKeyAuthentication
from tastypie import fields
from django.conf.urls import url
from tastypie.utils import trailing_slash
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from tastypie.http import HttpGone, HttpMultipleChoices


class OrganizationResource(ModelResource):
    class Meta:
        queryset = Organization.objects.all()
        resource_name = 'organization'

        authorization= Authorization()
        authentication = ApiKeyAuthentication()

        def obj_create(self, bundle, request=None, **kwargs):
            return super(OrganizationResource, self).obj_create(bundle, request, user=request.user)

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'

        authorization= Authorization()
        authentication = ApiKeyAuthentication()

        def obj_create(self, bundle, request=None, **kwargs):
            return super(UserResource, self).obj_create(bundle, request, user=request.user)

        def apply_authorization_limits(self, request, object_list):
            return object_list.filter(id=request.user.id)

class CourseResource(ModelResource):
    class Meta:
        queryset = Course.objects.all()
        resource_name = 'course'

        authorization= Authorization()
        authentication = ApiKeyAuthentication()

        def obj_create(self, bundle, request=None, **kwargs):
            return super(CourseResource, self).obj_create(bundle, request, user=request.user)

        def apply_authorization_limits(self, request, object_list):
            return object_list.filter(organization=request.user.get_profile().organization)

class ProblemResource(ModelResource):
    essays = fields.ManyToManyField('freeform_data.api.EssayResource', 'problem', full=True)
    class Meta:
        queryset = Problem.objects.all()
        resource_name = 'problem'

        authorization= Authorization()
        authentication = ApiKeyAuthentication()

        def obj_create(self, bundle, request=None, **kwargs):
            return super(ProblemResource, self).obj_create(bundle, request, user=request.user)

        def apply_authorization_limits(self, request, object_list):
            return object_list.filter(course__in=request.user.get_profile().organization.course_set)

class EssayResource(ModelResource):
    essay_grades = fields.ManyToManyField('freeform_data.api.EssayGradeResource', 'essay', full=True)
    user = fields.ForeignKey(UserResource, 'user')
    class Meta:
        queryset = Essay.objects.all()
        resource_name = 'essay'

        authorization= Authorization()
        authentication = ApiKeyAuthentication()

        def obj_create(self, bundle, request=None, **kwargs):
            return super(EssayResource, self).obj_create(bundle, request, user=request.user)

        def apply_authorization_limits(self, request, object_list):
            return object_list.filter(user__id=request.user.id)

class EssayGradeResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    class Meta:
        queryset = EssayGrade.objects.all()
        resource_name = 'essay_grade'

        authorization= Authorization()
        authentication = ApiKeyAuthentication()

        def obj_create(self, bundle, request=None, **kwargs):
            return super(EssayGradeResource, self).obj_create(bundle, request, user=request.user)

        def apply_authorization_limits(self, request, object_list):
            return object_list.filter(essay__user__id=request.user.id|user__id=request.user.id)

class EssaySetResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    essays = fields.ManyToManyField('essay_api.api.EssayResource', 'essay_set', full=True)

    class Meta:
        queryset = EssaySet.objects.all()
        resource_name = 'essay_set'

        allowed_methods = ['get', 'post', 'delete']
        fields = ['prompt', 'scale_type', 'grader_type', 'min_score', 'max_score', 'description', 'name', 'date_modified', 'date_created']

        authorization= Authorization()
        authentication = ApiKeyAuthentication()


    def obj_create(self, bundle, request=None, **kwargs):
        return super(EssaySetResource, self).obj_create(bundle, request, user=request.user)

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user__id=request.user.id)