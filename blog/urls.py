
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.blog_index,name="blog_index"),
    path("post/<int:pk>/",views.blog_detail,name="blog_detail"),
    path("category/<category>/",views.blog_category,name="blog_category"),
    path('register/', views.register, name='register'),  # URL for the registration page
    path('login/', views.user_login, name='login'),  
    path('logout/', auth_views.LogoutView.as_view(next_page='blog_index'), name='logout'),  
    path('create/', views.create_post, name='create_post'),
      # urls.py
]
