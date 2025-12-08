from django.urls import path
from .views import RegisterView, LoginView, LogoutView
from .views_admin import UserListView, UserToggleActiveView, UserDeleteView, UserCreateView

urlpatterns = [
    # path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Admin User Management
    path('admin/users/', UserListView.as_view(), name='admin_user_list'),
    path('admin/users/create/', UserCreateView.as_view(), name='admin_user_create'),
    path('admin/users/<int:pk>/toggle/', UserToggleActiveView.as_view(), name='admin_user_toggle'),
    path('admin/users/<int:pk>/delete/', UserDeleteView.as_view(), name='admin_user_delete'),
]
