from django.urls import path
from django.contrib.auth import views as auth_views
from videoapp import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='videoapp/login.html'), name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),  # Detail view URL for videos
    path('', views.search_videos, name='search_videos'),  # Your main search page URL
    # Other URLs for your app
]
