from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True 
        return request.user.is_authenticated and request.user.profile.role == "ADMIN"


class IsOwnerOrAdmin(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.profile.role == "ADMIN":
            return True  
        return obj.created_by == request.user  

class IsOwnerOrAdminForAnswer(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.profile.role == "ADMIN":
            return True 
        return obj.answered_by == request.user 


class IsAuthenticatedAndCanVote(permissions.BasePermission):
    

    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.is_staff
    
    # def has_object_permission(self, request, view, obj):
    #     if self.

class CanGenerateOrViewReport(permissions.BasePermission):
    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.question.created_by == request.user  or request.user.is_staff  
        return request.user.is_staff