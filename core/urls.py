from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-admin/', views.create_admin, name='create_admin'),
    # path('permission/', views.permission, name='permission'),
    # path('group_permission/', views.group_permission, name='group_permission'),
    # path('new_user/', views.new_user, name='new_user'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-profile/', views.create_profile, name='create_profile'),
    
    path('add-blog/', views.add_blog, name='add_blog'),
    path('view-blog/', views.view_blog, name='view_blog'),
    path('update_blog/<int:id>/', views.update_blog, name='update_blog'),
    path('delete_blog/<int:id>/', views.delete_blog, name='delete_blog'),
]
