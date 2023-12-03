from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('process_order/', process_order, name='process_order'),
    path('me/', OrderList.as_view(), name='order_list'),
    path('<int:pk>', OrderDetail.as_view(), name='order_detail'),
    
    path('validarCarrito/', validarCarrito, name='validarCarrito'),
]
