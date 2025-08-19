from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product_details/', views.product_details, name='product_details'),
    path('products/<int:category_id>/', views.products_by_category, name='products_by_category'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/',views.cart, name='cart'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
   
]