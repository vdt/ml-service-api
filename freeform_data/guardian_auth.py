from tastypie.authorization import Authorization
from tastypie.exceptions import TastypieError, Unauthorized
from guardian.core import ObjectPermissionChecker
import logging
logger = logging.getLogger(__name__)

def check_permissions(permission_type,user,obj):
    checker = ObjectPermissionChecker(user)
    class_lower_name = obj.__class__.__name__.lower()
    perm = '{0}_{1}'.format(permission_type, class_lower_name)
    return checker.has_perm(perm,obj)

class GuardianAuthorization(Authorization):
    """
      Uses permission checking from ``django.contrib.auth`` to map
      ``POST / PUT / DELETE / PATCH`` to their equivalent Django auth
      permissions.

      Both the list & detail variants simply check the model they're based
      on, as that's all the more granular Django's permission setup gets.
      """
    def base_checks(self, request, model_klass):

        # If it doesn't look like a model, we can't check permissions.
        if not model_klass or not getattr(model_klass, '_meta', None):
            return False

        # User must be logged in to check permissions.
        if not hasattr(request, 'user'):
            return False

        return model_klass

    def read_list(self, object_list, bundle):
        klass = self.base_checks(bundle.request, object_list.model)
        read_list=[]

        if klass is False:
            return []

        for obj in object_list:
            if check_permissions("view", bundle.request.user, obj):
                read_list.append(obj)
        # GET-style methods are always allowed.
        return read_list

    def read_detail(self, object_list, bundle):
        klass = self.base_checks(bundle.request, bundle.obj.__class__)
        read_list=[]


        if klass is False:
            raise Unauthorized("You are not allowed to access that resource.")

        for obj in object_list:
            if check_permissions("view", bundle.request.user, obj):
                read_list.append(obj)

        return True

    def create_list(self, object_list, bundle):
        klass = self.base_checks(bundle.request, object_list.model)
        create_list=[]

        if klass is False:
            return []

        for obj in object_list:
            #if check_permissions("add", bundle.request.user, obj):
            create_list.append(obj)

        return create_list

    def create_detail(self, object_list, bundle):
        klass = self.base_checks(bundle.request, bundle.obj.__class__)
        create_list=[]

        if klass is False:
            raise Unauthorized("You are not allowed to access that resource.")

        for obj in object_list:
            #if check_permissions("add", bundle.request.user, obj):
            create_list.append(obj)

        return True

    def update_list(self, object_list, bundle):
        klass = self.base_checks(bundle.request, object_list.model)
        update_list=[]

        if klass is False:
            return []

        for obj in object_list:
            if check_permissions("change", bundle.request.user, obj):
                update_list.append(obj)

        if update_list:
            return update_list
        raise Unauthorized("You are not allowed to access that resource.")

    def update_detail(self, object_list, bundle):
        update_list=[]
        klass = self.base_checks(bundle.request, bundle.obj.__class__)

        if klass is False:
            raise Unauthorized("You are not allowed to access that resource.")

        for obj in object_list:
            if check_permissions("change", bundle.request.user, obj):
                update_list.append(obj)

        if update_list:
            return update_list
        raise Unauthorized("You are not allowed to access that resource.")

    def delete_list(self, object_list, bundle):
        delete_list=[]
        klass = self.base_checks(bundle.request, object_list.model)

        if klass is False:
            return []

        for obj in object_list:
            if check_permissions("delete", bundle.request.user, obj):
                delete_list.append(obj)

        if delete_list:
            return delete_list
        raise Unauthorized("You are not allowed to access that resource.")

    def delete_detail(self, object_list, bundle):
        delete_list=[]

        klass = self.base_checks(bundle.request, bundle.obj.__class__)

        if klass is False:
            raise Unauthorized("You are not allowed to access that resource.")

        for obj in object_list:
            if check_permissions("delete", bundle.request.user, obj):
                delete_list.append(obj)

        if delete_list:
            return delete_list
        raise Unauthorized("You are not allowed to access that resource.")
