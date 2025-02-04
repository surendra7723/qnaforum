from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Read permissions for everyone
        return request.user.is_authenticated and request.user.profile.role == "ADMIN"


class IsOwnerOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user == obj.created_by or request.user.profile.role == "ADMIN"
        )


class IsQuestionApprovedOrOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            obj.status == "APPROVED" or 
            request.user==obj.created_by or 
            getattr(request.user, "profile", None) and request.user.profile.role == "ADMIN"
        )

class CanVoteOnQuestion(permissions.BasePermission):


    def has_permission(self, request, view):
        return request.user.is_authenticated


class CanVoteOnAnswer(permissions.BasePermission):


    def has_permission(self, request, view):
        return request.user.is_authenticated


