from django.urls import path
from . import views

urlpatterns = [
    path('add-category/', views.add_category, name='add_category'),
    path('view-categories/', views.view_categories, name='view_categories'),
    path('category/edit/<int:pk>/', views.update_category, name='update_category'),  
    path('category/delete/<int:pk>/', views.delete_category, name='delete_category'),
    
    path('add-subcategory/', views.add_subcategory, name='add_subcategory'),
    path('view-subcategories/', views.view_subcategories, name='view_subcategories'),
    path('edit-subcategory/<int:id>/', views.edit_subcategory, name='edit_subcategory'),
    path('delete-subcategory/<int:id>/', views.delete_subcategory, name='delete_subcategory'),
    
    path('add-product/', views.add_product, name='add_product'),
    path('view-products/', views.view_products, name='view_products'),
    path('get-subcategories/', views.get_subcategories, name='get_subcategories'),
    path('products/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:pk>/', views.delete_product, name='delete_product'),
    
    path('inventory_dashboard/', views.inventory_dashboard, name='inventory_dashboard'),
    
]
