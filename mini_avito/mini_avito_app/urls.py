from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'User', views.UserViewSet)
router.register(r'Client', views.ClientViewSet)
router.register(r'Products', views.ProductViewSet)
router.register(r'Category_product', views.Category_productViewSet)
router.register(r'Order', views.OrderViewSet)

urlpatterns = [
    path('rest/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', views.custom_main, name='homepage'),
    path('profile/', views.profile, name='profile'),
    path('product_list/', views.products_list, name='product_list'),
    path('product/<str:p_id>', views.product_page, name='product'),
    path('my_products/', views.my_products_page, name='my_products'),
    path('my_orders/', views.my_orders_page, name='my_orders'),
    path('my_sales/', views.my_sales_page, name='my_sales'),
    path('get_money/', views.get_money, name='get_money'),
    path('create_product/', views.create_product, name='create_product'),
]
