from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    # path('products/', views.manage_products, name='manage_products'),
    path('customers/', views.manage_customers, name='manage_customers'),
    
    # path('orders/', views.manage_orders, name='manage_orders'),
    path('customers/', views.manage_customers, name='manage_customers'),
    # path('create-employee/', views.create_employee, name='create_employee'),
    path('create_permission/', views.create_permission, name='create_permission'),
    path('manage_permissions/', views.manage_permissions, name='manage_permissions'),
    

    path('permissions/edit/<int:role_id>/', views.edit_role_permissions, name='edit_role_permissions'),
    path('permissions/delete/<int:role_id>/', views.delete_role, name='delete_role'),
    
    path('create-employee/', views.create_employee, name='create_employee'),
    path('manage-employees/', views.manage_employees, name='manage_employees'),
    
    path('edit-employee/<int:user_id>/', views.edit_employee, name='edit_employee'),
    path('delete-employee/<int:user_id>/', views.delete_employee, name='delete_employee'),
    
    path("order_list/", views.order_list, name="order_list"),
    path('orders/delete/<int:order_id>/', views.delete_order, name='delete_order'),
    
   
]