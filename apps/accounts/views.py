from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone

from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    UserListSerializer,
    PasswordChangeSerializer
)
from .permissions import IsOwner, IsAdminOrOwner

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user' : UserSerializer(user).data,
            'refresh': str(refresh),
            'access':str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
        
class UserProfileView(generics.RetrieveAPIView):
    
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
class UserUpdateProfileView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
class PasswordChangeView(generics.GenericAPIView):
    
    serializer_class = PasswordChangeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self,request,*args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response(
            {'message' : 'Password changed successfully.'},
            status=status.HTTP_200_OK
        )
        
class UserListView(generics.ListAPIView):
    
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrOwner]
    
    def get_queryset(self):
        queryset = User.objects.all()
        
        # Filter by role
        role = self.request.query_params.get('role')
        if role:
            queryset = queryset.filter(role=role)
        
        # Filter by status
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        # Search
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(phone__icontains=search) |
                Q(employee_id__icontains=search)
            )
        
        return queryset.order_by('-date_joined')
    

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating and deleting a user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrOwner]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer
    
    def perform_destroy(self, instance):
        # Soft delete - deactivate user
        instance.is_active = False
        instance.save()


class WorkerListView(generics.ListAPIView):
    """
    API endpoint for listing workers.
    """
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        return User.objects.filter(role='worker').order_by('-date_joined')


class OwnerListView(generics.ListAPIView):
    """
    API endpoint for listing owners.
    """
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrOwner]
    
    def get_queryset(self):
        return User.objects.filter(role='owner').order_by('-date_joined')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def verify_worker(request, pk):
    """
    API endpoint for verifying a worker.
    Only owners can verify workers.
    """
    if not request.user.is_owner:
        return Response(
            {'error': 'Only owners can verify workers.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        worker = User.objects.get(pk=pk, role='worker')
    except User.DoesNotExist:
        return Response(
            {'error': 'Worker not found.'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    worker.is_verified = True
    worker.save()
    
    return Response(
        {'message': 'Worker verified successfully.'},
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_stats(request):
    """
    API endpoint for getting user statistics.
    """
    user = request.user
    
    stats = {
        'total_owners': User.objects.filter(role='owner').count() if user.is_owner else None,
        'total_workers': User.objects.filter(role='worker').count() if user.is_owner else None,
        'active_workers': User.objects.filter(role='worker', is_active=True).count() if user.is_owner else None,
        'pending_verifications': User.objects.filter(role='worker', is_verified=False).count() if user.is_owner else None,
    }
    
    return Response(stats, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """
    API endpoint for logging out (blacklisting refresh token).
    """
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        # Update last login
        request.user.last_login = timezone.now()
        request.user.save()
        
        return Response(
            {'message': 'Logged out successfully.'},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )