from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOrganizerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.organizer==request.user

class IsConfirmedOrReadOnly(BasePermission):
    def has_object_permission(self, request, view,obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user ==  obj.user
