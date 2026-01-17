"""
JWT Authentication Middleware for Django Views
Allows JWT tokens to be used for authentication in traditional Django views
"""
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin


class JWTAuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware to authenticate users via JWT tokens in traditional Django views
    """
    def process_request(self, request):
        """
        Process the request and authenticate user if JWT token is present
        """
        # Skip if user is already authenticated via session
        if hasattr(request, 'user') and request.user.is_authenticated:
            return None
        
        # Get token from Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header.startswith('Bearer '):
            return None
        
        # Extract token
        token = auth_header.split(' ')[1] if len(auth_header.split(' ')) > 1 else None
        
        if not token:
            return None
        
        # Authenticate using JWT
        jwt_auth = JWTAuthentication()
        try:
            validated_token = jwt_auth.get_validated_token(token)
            user = jwt_auth.get_user(validated_token)
            request.user = user
        except (InvalidToken, TokenError):
            # Token is invalid, leave user as anonymous
            pass
        except Exception:
            # Any other error, leave user as anonymous
            pass
        
        return None

