# custom permissions
from rest_framework import permissions

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
        return request.user.has_perm('your_app.can_verify_client')

class CanRecordLeads(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('your_app.can_record_leads')

class CanCommunicateTerms(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('your_app.can_communicate_terms')

class CanGuidePosting(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('your_app.can_guide_posting')

class CanApproveListings(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('your_app.can_approve_listings')

class CanEditDescriptions(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('your_app.can_edit_descriptions')

class CanShareClientInfo(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('your_app.can_share_client_info')

class CanRemindPosting(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('your_app.can_remind_posting')

class CanRequestPropertyInfo(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('your_app.can_request_property_info')

class CanMonitorSatisfaction(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('your_app.can_monitor_satisfaction')

class CanRecordTenantMoveIn(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('your_app.can_record_tenant_move_in')

class CanInvoiceClients(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('your_app.can_invoice_clients')

class CanRecordPayments(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('your_app.can_record_payments')

class CanBanNonPayingClients(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('your_app.can_ban_nonpaying_clients')