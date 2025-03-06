# custom permissions
from rest_framework import permissions
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

class IsApprovedPermissions(permissions.DjangoModelPermissions):
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
        if request.method in permissions.SAFE_METHODS:
            return True
        user= request.user
        print(request.user.is_authenticated)
        if request.user.is_authenticated:
            if user.approval_status == "APPROVED":
                return True

        return  False



class CanVerifyClient(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        user = request.user
        if not user.is_authenticated:
            return False

        try:
            # Get the permission object
            content_type = ContentType.objects.get(app_label='listing', model='property') #replace your_model_name
            permission = Permission.objects.get(codename='can_verify_client', content_type=content_type)

            # Check if the user has the permission directly or through a group
            return user.has_perm('listing.can_verify_client') and permission in user.user_permissions.all() or user.groups.filter(permissions=permission).exists()

        except (ContentType.DoesNotExist, Permission.DoesNotExist):
            # Handle cases where the content type or permission doesn't exist
            return False
 


class CanRecordLeads(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.has_perm('listing.can_record_leads')

class CanCommunicateTerms(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.has_perm('listing.can_communicate_terms')

class CanGuidePosting(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.has_perm('listing.can_guide_posting')

class CanApproveListings(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        user = request.user
        if not user.is_authenticated:
            return False

        try:
            # Get the permission object
            content_type = ContentType.objects.get(app_label='listing', model='property') #replace your_model_name
            permission = Permission.objects.get(codename='can_approve_listings', content_type=content_type)

            # Check if the user has the permission directly or through a group
            return user.has_perm(f'listing.can_approve_listings') and permission in user.user_permissions.all() or user.groups.filter(permissions=permission).exists()

        except (ContentType.DoesNotExist, Permission.DoesNotExist):
            # Handle cases where the content type or permission doesn't exist
            return False
     

class CanEditDescriptions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user
        if not user.is_authenticated:
            return False

        try:
            # Get the permission object
            content_type = ContentType.objects.get(app_label='listing', model='property') #replace your_model_name
            permission = Permission.objects.get(codename='can_edit_descriptions', content_type=content_type)

            # Check if the user has the permission directly or through a group
            return user.has_perm(f'listing.can_edit_descriptions') and permission in user.user_permissions.all() or user.groups.filter(permissions=permission).exists()

        except (ContentType.DoesNotExist, Permission.DoesNotExist):
            # Handle cases where the content type or permission doesn't exist
            return False



class CanShareClientInfo(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        user = request.user
        if not user.is_authenticated:
            return False

        try:
            content_type = ContentType.objects.get(app_label='listing', model='property') #replace your_model_name
            permission = Permission.objects.get(codename='can_share_client_info', content_type=content_type)

            # Check if the user has the permission directly or through a group
            # Check if the user has the permission directly or through a group
            return user.has_perm('listing.can_share_client_info') and permission in user.user_permissions.all() or user.groups.filter(permissions=permission).exists()

        except (ContentType.DoesNotExist, Permission.DoesNotExist):
            # Handle cases where the content type or permission doesn't exist
            return False
       

class CanRemindPosting(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        

        user = request.user
        if not user.is_authenticated:
            return False

        try:
            # Get the permission object
            content_type = ContentType.objects.get(app_label='listing', model='property') #replace your_model_name
            permission = Permission.objects.get(codename='can_remind_posting', content_type=content_type)


            # Check if the user has the permission directly or through a group
            return user.has_perm('listing.can_remind_posting') and permission in user.user_permissions.all() or user.groups.filter(permissions=permission).exists()

        except (ContentType.DoesNotExist, Permission.DoesNotExist):
            # Handle cases where the content type or permission doesn't exist
            return False
       

class CanRequestPropertyInfo(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        user = request.user
        if not user.is_authenticated:
            return False

        try:
            # Get the permission object
             
            content_type = ContentType.objects.get(app_label='listing', model='property') #replace your_model_name
            permission = Permission.objects.get(codename='can_request_property_info', content_type=content_type)

            # Check if the user has the permission directly or through a group
            return user.has_perm('listing.can_request_property_info') and permission in user.user_permissions.all() or user.groups.filter(permissions=permission).exists()

        except (ContentType.DoesNotExist, Permission.DoesNotExist):
            # Handle cases where the content type or permission doesn't exist
            return False


class CanMonitorSatisfaction(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        user = request.user
        if not user.is_authenticated:
            return False

        try:
            # Get the permission object
            content_type = ContentType.objects.get(app_label='listing', model='property') #replace your_model_name
            permission = Permission.objects.get(codename='can_monitor_satisfaction', content_type=content_type)

            # Check if the user has the permission directly or through a group
            return user.has_perm('listing.can_monitor_satisfaction') and permission in user.user_permissions.all() or user.groups.filter(permissions=permission).exists()

        except (ContentType.DoesNotExist, Permission.DoesNotExist):
            # Handle cases where the content type or permission doesn't exist
            return False
 

class CanRecordTenantMoveIn(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
    

        user = request.user
        if not user.is_authenticated:
            return False

        try:
            # Get the permission object
            content_type = ContentType.objects.get(app_label='listing', model='property') #replace your_model_name
            permission = Permission.objects.get(codename='can_record_tenant_move_in', content_type=content_type)

            # Check if the user has the permission directly or through a group
            return user.has_perm('listing.can_record_tenant_move_in') and permission in user.user_permissions.all() or user.groups.filter(permissions=permission).exists()

        except (ContentType.DoesNotExist, Permission.DoesNotExist):
            # Handle cases where the content type or permission doesn't exist
            return False
 

class CanInvoiceClients(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        user = request.user
        if not user.is_authenticated:
            return False

        try:
            # Get the permission object
            content_type = ContentType.objects.get(app_label='listing', model='property') #replace your_model_name
            permission = Permission.objects.get(codename='can_invoice_clients', content_type=content_type)

            # Check if the user has the permission directly or through a group
            return user.has_perm('listing.can_invoice_clients') and permission in user.user_permissions.all() or user.groups.filter(permissions=permission).exists()

        except (ContentType.DoesNotExist, Permission.DoesNotExist):
            # Handle cases where the content type or permission doesn't exist
            return False
 

class CanRecordPayments(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        user = request.user
        if not user.is_authenticated:
            return False

        try:
            # Get the permission object
            content_type = ContentType.objects.get(app_label='listing', model='property') #replace your_model_name
            permission = Permission.objects.get(codename='can_record_payments', content_type=content_type)

            # Check if the user has the permission directly or through a group
            return user.has_perm('listing.can_record_payments') and permission in user.user_permissions.all() or user.groups.filter(permissions=permission).exists()

        except (ContentType.DoesNotExist, Permission.DoesNotExist):
            # Handle cases where the content type or permission doesn't exist
            return False
 


class CanBanNonPayingClients(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
    
        user = request.user
        if not user.is_authenticated:
            return False

        try:
            # Get the permission object
            content_type = ContentType.objects.get(app_label='listing', model='property') #replace your_model_name
            permission = Permission.objects.get(codename='can_ban_nonpaying_clients', content_type=content_type)

            # Check if the user has the permission directly or through a group
            return user.has_perm('listing.can_ban_nonpaying_clients') and permission in user.user_permissions.all() or user.groups.filter(permissions=permission).exists()

        except (ContentType.DoesNotExist, Permission.DoesNotExist):
            # Handle cases where the content type or permission doesn't exist
            return False
