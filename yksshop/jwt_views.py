"""
JWT Authentication Views
Provides JWT token endpoints for authentication
"""
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom token serializer to include additional user data"""
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['is_staff'] = user.is_staff
        
        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom token obtain view with additional user data in response"""
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(
                {'error': 'Invalid credentials', 'detail': str(e)},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Get user data
        user = User.objects.get(username=serializer.validated_data['username'])
        
        return Response({
            'access': serializer.validated_data['access'],
            'refresh': serializer.validated_data['refresh'],
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_staff': user.is_staff,
            }
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def jwt_login(request):
    """
    JWT Login endpoint
    Accepts: email/username and password
    Returns: JWT tokens and user data
    """
    email_or_username = request.data.get('email') or request.data.get('username')
    password = request.data.get('password')
    
    if not email_or_username or not password:
        return Response(
            {'error': 'Email/username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Try to authenticate with email or username
    user = None
    try:
        # Try email first
        user = User.objects.get(email=email_or_username)
        user = authenticate(username=user.username, password=password)
    except User.DoesNotExist:
        # Try username
        user = authenticate(username=email_or_username, password=password)
    
    if not user:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    if not user.is_active:
        return Response(
            {'error': 'User account is disabled'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Generate tokens using serializer
    serializer = CustomTokenObtainPairSerializer()
    token = serializer.get_token(user)
    
    return Response({
        'access': str(token.access_token),
        'refresh': str(token),
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_staff': user.is_staff,
        }
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def jwt_user_info(request):
    """
    Get current user information from JWT token
    """
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_staff': user.is_staff,
        'is_active': user.is_active,
    }, status=status.HTTP_200_OK)

