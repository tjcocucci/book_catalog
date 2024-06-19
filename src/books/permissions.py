import requests
from rest_framework import permissions
from django.conf import settings


class AuthServerPermission(permissions.BasePermission):
    """
    Global permission check for blocked IPs.
    """

    def has_permission(self, request, view):

        if "Authorization" not in request.headers:
            return False

        try:
            response = requests.get(
                f"{settings.AUTH_SERVER_URL}/session/",
                headers={"Authorization": request.headers["Authorization"]},
            )
        except requests.exceptions.RequestException as e:
            print(e)
            return False

        if not response.ok:
            return False

        return True
