from oauth2_provider.contrib.rest_framework import TokenHasScope, OAuth2Authentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS


class TokenHasAdminScope(TokenHasScope):
    def get_scopes(self, request, view):
        return ["admin"]


class UserReadsAdminWrites(IsAuthenticatedOrReadOnly):
    def is_oauth2_authenticated(self, request):
        return isinstance(request.successful_authenticator, OAuth2Authentication)

    def has_permission(self, request, view):
        is_read = request.method in SAFE_METHODS and self.is_oauth2_authenticated(request)
        is_admin = TokenHasAdminScope().has_permission(request, view)
        return is_read or is_admin
