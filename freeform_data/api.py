from tastypie.resources import ModelResource, Resource
from freeform_data.models import Organization, UserProfile, Course, Problem, Essay, EssayGrade, Membership, UserRoles
from django.contrib.auth.models import User
from tastypie.authorization import Authorization, DjangoAuthorization
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


class SessionAuthentication(Authentication):
    """
    Override session auth to always return the auth status
    """
    def is_authenticated(self, request, **kwargs):
        """
        Checks to make sure the user is logged in & has a Django session.
        """
        return request.user.is_authenticated()

    def get_identifier(self, request):
        """
        Provides a unique string identifier for the requestor.
        This implementation returns the user's username.
        """
        return request.user.username

def default_authorization():
    """
    Used to ensure that changing authorization can be done on a sitewide level easily.
    """
    return Authorization()

def default_authentication():
    """
    Ensures that authentication can easily be changed on a sitewide level.
    """
    return MultiAuthentication(SessionAuthentication(), ApiKeyAuthentication())

def default_serialization():
    """
    Current serialization formats.  HTML is not supported for now.
    """
    return Serializer(formats=['json', 'jsonp', 'xml', 'yaml', 'html', 'plist'])

class CreateUserResource(ModelResource):
    """
    Creates a user with the specified username and password.  This is needed because of permissions restrictions
    on the normal user resource.
    """
    class Meta:
        allowed_methods = ['post']
        object_class = User
        #No authentication for create user, or authorization.  Anyone can create.
        authentication = Authentication()
        authorization = Authorization()
        fields = ['username']
        resource_name = "createuser"
        always_return_data = True

    def obj_create(self, bundle, **kwargs):
        username, password = bundle.data['username'], bundle.data['password']
        try:
            bundle.obj = User.objects.create_user(username, '', password)
        except IntegrityError:
            raise BadRequest('That username already exists')
        return bundle

class OrganizationResource(ModelResource):
    """
    Preserves appropriate many to many relationships, and encapsulates the Organization model.
    """
    courses = fields.ToManyField('freeform_data.api.CourseResource', 'course_set', null=True)
    essays = fields.ToManyField('freeform_data.api.EssayResource', 'essay_set', null=True)
    #This maps the organization users to the users model via membership
    user_query = lambda bundle: bundle.obj.users.through.objects.all() or bundle.obj.users
    users = fields.ToManyField("freeform_data.api.MembershipResource", attribute=user_query, null=True)
    #Also show members in the organization (useful for getting role)
    memberships = fields.ToManyField("freeform_data.api.MembershipResource", 'membership_set', null=True)
    class Meta:
        queryset = Organization.objects.all()
        resource_name = 'organization'

        serializer = default_serialization()
        authorization= default_authorization()
        authentication = default_authentication()
        always_return_data = True

    def obj_create(self, bundle, **kwargs):
        bundle = super(OrganizationResource, self).obj_create(bundle)
        return bundle

    def save_m2m(self,bundle):
        """
        Save_m2m saves many to many models.  This hack adds a membership object, which is needed, as membership
        is the relation through which organization is connected to user.
        """
        add_membership(bundle.request.user, bundle.obj)
        bundle.obj.save()

    def dehydrate_users(self, bundle):
        """
        Tastypie will currently show memberships instead of users due to the through relation.
        This hacks the relation to show users.
        """
        if bundle.data.get('users'):
            log.debug(bundle.data.get('users'))
            l_users = bundle.obj.users.all()
        resource_uris = []
        user_resource = UserResource()
        for l_user in l_users:
            resource_uris.append(user_resource.get_resource_uri(bundle_or_obj=l_user))
        return resource_uris

class UserProfileResource(ModelResource):
    """
    Encapsulates the UserProfile module
    """
    user = fields.ToOneField('freeform_data.api.UserResource', 'user', related_name='userprofile')
    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = 'userprofile'

        serializer = default_serialization()
        authorization= default_authorization()
        authentication = default_authentication()
        always_return_data = True

    def obj_create(self, bundle, request=None, **kwargs):
        return super(UserProfileResource, self).obj_create(bundle,user=bundle.request.user)

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user_id=request.user.id)

class UserResource(ModelResource):
    """
    Encapsulates the User Model
    """
    essaygrades = fields.ToManyField('freeform_data.api.EssayGradeResource', 'essaygrade_set', null=True, related_name='user')
    essays = fields.ToManyField('freeform_data.api.EssayResource', 'essay_set', null=True, related_name='user')
    courses = fields.ToManyField('freeform_data.api.CourseResource', 'course_set', null=True)
    userprofile = fields.ToOneField('freeform_data.api.UserProfileResource', 'userprofile', related_name='user')
    organizations = fields.ToManyField('freeform_data.api.OrganizationResource', 'organization_set', null=True)
    memberships = fields.ToManyField("freeform_data.api.MembershipResource", 'membership_set', null=True)
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'

        serializer = default_serialization()
        authorization= default_authorization()
        authentication = default_authentication()
        always_return_data = True

    def obj_create(self, bundle, **kwargs):
        return super(UserResource, self).obj_create(bundle)

    def dehydrate(self, bundle):
        bundle.data['api_key'] = bundle.obj.api_key.key
        return bundle

    def apply_authorization_limits(self, request, object_list):
        log.debug("Applying limits.")
        return object_list.filter(user_id=request.user.id)

class MembershipResource(ModelResource):
    """
    Encapsulates the Membership Model
    """
    user = fields.ToOneField('freeform_data.api.UserResource', 'user')
    organization = fields.ToOneField('freeform_data.api.OrganizationResource', 'organization')
    class Meta:
        queryset = Membership.objects.all()
        resource_name = 'membership'

        serializer = default_serialization()
        authorization= default_authorization()
        authentication = default_authentication()
        always_return_data = True

    def obj_create(self, bundle, request=None, **kwargs):
        return super(MembershipResource, self).obj_create(bundle,user=bundle.request.user)

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user_id=request.user.id)

class CourseResource(ModelResource):
    """
    Encapsulates the Course Model
    """
    organizations = fields.ToManyField(OrganizationResource, 'organizations', null=True)
    users = fields.ToManyField(UserResource, 'users', null=True)
    problems = fields.ToManyField('freeform_data.api.ProblemResource', 'problem_set', null=True)
    class Meta:
        queryset = Course.objects.all()
        resource_name = 'course'

        serializer = default_serialization()
        authorization= default_authorization()
        authentication = default_authentication()
        always_return_data = True

    def obj_create(self, bundle, **kwargs):
        return super(CourseResource, self).obj_create(bundle, user=bundle.request.user)

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(organization__in=request.user.organizations)

class ProblemResource(ModelResource):
    """
    Encapsulates the problem Model
    """
    essays = fields.ToManyField('freeform_data.api.EssayResource', 'essay_set', null=True, related_name='problem')
    courses = fields.ToManyField('freeform_data.api.CourseResource', 'courses')
    class Meta:
        queryset = Problem.objects.all()
        resource_name = 'problem'

        serializer = default_serialization()
        authorization= default_authorization()
        authentication = default_authentication()
        always_return_data = True

    def obj_create(self, bundle, **kwargs):
        return super(ProblemResource, self).obj_create(bundle)

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(course__in=request.user.organizations.courses)

class EssayResource(ModelResource):
    """
    Encapsulates the essay Model
    """
    essaygrades = fields.ToManyField('freeform_data.api.EssayGradeResource', 'essaygrade_set', null=True, related_name='essay')
    user = fields.ToOneField(UserResource, 'user', null=True)
    organization = fields.ToOneField(OrganizationResource, 'organization', null=True)
    problem = fields.ToOneField(ProblemResource, 'problem')
    class Meta:
        queryset = Essay.objects.all()
        resource_name = 'essay'

        serializer = default_serialization()
        authorization= default_authorization()
        authentication = default_authentication()
        always_return_data = True

    def obj_create(self, bundle, **kwargs):
        bundle = super(EssayResource, self).obj_create(bundle, user=bundle.request.user)
        bundle.obj.user = bundle.request.user
        bundle.obj.save()

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user_id=request.user.id)

class EssayGradeResource(ModelResource):
    """
    Encapsulates the EssayGrade Model
    """
    user = fields.ToOneField(UserResource, 'user', null=True)
    essay = fields.ToOneField(EssayResource, 'essay')
    class Meta:
        queryset = EssayGrade.objects.all()
        resource_name = 'essaygrade'

        serializer = default_serialization()
        authorization= default_authorization()
        authentication = default_authentication()
        always_return_data = True

    def obj_create(self, bundle, **kwargs):
        bundle = super(EssayGradeResource, self).obj_create(bundle, user=bundle.request.user)
        bundle.obj.user = bundle.request.user
        bundle.obj.save()
        return bundle

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(essay__user_id=Q(request.user.id)|Q(user_id=request.user.id))

def add_membership(user,organization):
    """
    Adds a membership object.  Required because membership defines the relation between user and organization,
    and tastypie does not automatically create through relations.
    """
    users = organization.users.all()
    membership = Membership(
        user = user,
        organization = organization,
    )
    if users.count()==0:
        #If a user is the first one in an organization, make them the administrator.
        membership.role = UserRoles.administrator
        membership.save()
    else:
        membership.role = UserRoles.student
    membership.save()

