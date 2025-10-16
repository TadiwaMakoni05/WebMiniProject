from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('product-details/<int:product_id>/', views.product_details, name='product_details'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),


    # 👇 Admin CRUD URLs
    path('manage/products/', views.manage_products, name='manage_products'),
    path('manage/products/add/', views.add_product, name='add_product'),
    path('manage/products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('manage/products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
]
