# from django.urls import path
from django.contrib.auth import views as auth_views
# from videoapp import views

# urlpatterns = [
#     path('login/', auth_views.LoginView.as_view(template_name='videoapp/login.html'), name='login'),
#     path('signup/', views.signup, name='signup'),
#     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
#     path('artist-login/', auth_views.LoginView.as_view(template_name='videoapp/artist_login.html'), name='artist_login'),  # New Artist Login URL
#     path('video/<int:video_id>/', views.video_detail, name='video_detail'),  # Detail view URL for videos
#     path('artist-signup/', views.artist_signup, name='artist_signup'),  # Artist Signup URL
#     path('', views.search_videos, name='search_videos'),  # Your main search page URL
#     path('artist-dashboard/', views.artist_dashboard, name='artist_dashboard'),
#     path('get_subcategories/', views.get_subcategories, name='get_subcategories'),
#     path('get_tags/', views.get_tags, name='get_tags'),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='videoapp/login.html'), name='login'),
    path('signup/', views.signup, name='signup'),  # Regular signup for users
    path('artist-signup/', views.artist_signup, name='artist_signup'),  # Artist signup
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),  # Redirect based on user type
    path('artist-dashboard/', views.artist_dashboard, name='artist_dashboard'),  # Artist dashboard
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),  # User dashboard
    path('video-search/', views.search_videos, name='video_search'),  # Video search page for both users and artists
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),  # Video detail page
    path('get_subcategories/', views.get_subcategories, name='get_subcategories'),  # Ajax endpoint for subcategories
    path('get_tags/', views.get_tags, name='get_tags'),  # Ajax endpoint for tags
    path('', views.search_videos, name='search_videos'),  # Your main search page URL
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('artist-login/', auth_views.LoginView.as_view(template_name='videoapp/artist_login.html'), name='artist_login'),  # New Artist Login URL
]
