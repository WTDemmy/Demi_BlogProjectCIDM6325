from django.urls import path
from django.contrib.auth import views as auth_views
from . import views 
from .views import (
    home,
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    register,        # <-- custom user registration
    profile,          # <-- optional profile page
    logout_view      # <-- custom logout view
)

urlpatterns = [
    path('', home, name='home'),

    # Blog post routes
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/new/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),


    # Authentication routes
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),


    # Django built-in auth views
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
