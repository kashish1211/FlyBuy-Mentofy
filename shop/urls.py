from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:pk>/',views.product_detail, name='product-detail'),
    path('<int:pk>/addtocart',views.add_cart, name='add-to-cart'),
    path('<int:pk>/removefromcart',views.remove_cart, name='remove-from-cart'),
    path('cart/',views.cart_view, name = 'cart'),
    path('cart/update/<int:pk>/',views.update_cart, name='update-cart'),
    path('checkout/',views.checkout_view, name = 'checkout'),
    
]