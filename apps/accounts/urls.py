from django.urls import path
from . import views

urlpatterns = [
    
    # Authentication
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('logout/', views.logout_view, name='user-logout'),
    
    # Profile
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('profile/update/', views.UserUpdateProfileView.as_view(), name='user-profile-update'),
    path('password/change/', views.PasswordChangeView.as_view(), name='password-change'),
    
    # User Management
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('users/<int:pk>/verify/', views.verify_worker, name='worker-verify'),
    
    # Role-based lists
    path('workers/', views.WorkerListView.as_view(), name='worker-list'),
    path('owners/', views.OwnerListView.as_view(), name='owner-list'),
    
    # Stats
    path('stats/', views.get_user_stats, name='user-stats'),
    
]

