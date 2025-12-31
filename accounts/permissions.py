from rest_framework.permissions import BasePermission
from rest_framework import permissions
from memberships.models import Subscription
from django.utils import timezone


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser
    
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)

class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff

class IsAdminOrStaff(BasePermission):
    """
    Allows access to Admin OR Staff users
    """

    def has_permission(self, request, view):
        user = request.user
        return (
            user
            and user.is_authenticated
            and (user.is_staff or user.is_superuser)
        )
    


class HasActiveSubscription(BasePermission):
    """
    Allows access only to users with an active subscription.
    """

    message = "You must have an active subscription to book a class."

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_anonymous:
            return Subscription.objects.filter(
                user=user,
                is_active=True,
                end_date__gte=timezone.now().date()
            ).exists()

        return False