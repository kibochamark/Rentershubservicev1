# custom permissions
from rest_framework import permissions

class IsStaffEditorPermissions(permissions.DjangoModelPermissions):
    # Map methods into required permission codes.
    # Override this if you need to also provide 'view' permissions,
    # or if you want to provide custom permission codes.
    perms_map = {
        'GET': [],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    def has_permission(self, request, view):
        user= request.user
        if user.is_staff:
            # use perm -> app_name.verbname
            # if user.hasperm(accounts.view_account)
            return True
        return  True

