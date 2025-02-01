from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('chat/<str:username>/', views.room, name='room'),
    # path('login/', auth_views.LoginView.as_view(template_name='chat/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='chat/logout.html'), name='logout'),
]