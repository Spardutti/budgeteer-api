from urllib import request
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
    # Gives read permisisons to all users
    # ! we dont really want this
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permisions only for user
        return obj.user == request.user
    