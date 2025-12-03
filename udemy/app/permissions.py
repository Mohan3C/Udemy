from rest_framework.permissions import BasePermission

class Isstudent(BasePermission):
    def has_permission(self, request, view):
        return
        (request.user.is_authenticated
        and hasattr(request.user,'role') 
        and request.user.role.role=='student' 
        )
        