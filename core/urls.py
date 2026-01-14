from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('signup/', views.signup, name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    
    # Profile (more specific routes first)
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/followers/', views.followers_list, name='followers'),
    path('profile/<str:username>/following/', views.following_list, name='following'),
    path('profile/<str:username>/', views.profile, name='profile'),
    
    # Posts
    path('', views.feed, name='feed'),
    path('create-post/', views.create_post, name='create_post'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
    
    # Social
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    
    # Explore & Tags
    path('explore/', views.explore, name='explore'),
    path('tag/<str:tag_slug>/', views.tag_posts, name='tag_posts'),
    
    # Notifications
    path('notifications/', views.view_notifications, name='view_notifications'),
    
    # Messaging
    path('messages/', views.chat_list, name='chat_list'),
    path('chat/<str:username>/', views.chat, name='chat'),
    path('send-message/<str:username>/', views.send_message, name='send_message'),
    path('get-messages/<str:username>/', views.get_messages, name='get_messages'),
]
