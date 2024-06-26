from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('blogs/', views.blog_list, name='blog_list'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('blog/new/', views.blog_create, name='blog_create'),
    path('blog/<int:pk>/edit/', views.blog_edit, name='blog_edit'),
    path('blog/<int:pk>/delete/', views.blog_delete, name='blog_delete'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('accounts/profile/', views.profile, name='profile'), 
    path('profile/update/', views.update_profile, name='update_profile'),
    path('pages/', views.page_list, name='page_list'),
    path('pages/<int:pk>/', views.page_detail, name='page_detail'),
    path('pages/new/', views.page_create, name='page_create'),
    path('pages/<int:pk>/edit/', views.page_update, name='page_update'),
    path('pages/<int:pk>/delete/', views.page_delete, name='page_delete'),
    path('messages/', views.message_list, name='message_list'),
    path('messages/<int:pk>/', views.message_detail, name='message_detail'),
    path('messages/new/', views.message_send, name='message_send'),
]

