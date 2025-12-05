
from rest_framework.permissions import BasePermission

class Isstudent(BasePermission):
    def has_permission(self, request, view):
        return
        (request.user.is_authenticated
        and hasattr(request.user,'role') 
        and request.user.role.role=='student' 
        )

class IsTeacher(BasePermission):
     message = "Access denied: Only teachers can perform this action."

     def has_permission(self, request, view):
        return (request.user.is_authenticated and hasattr(request.user, 'role') and request.user.role.role=="teacher" )

        