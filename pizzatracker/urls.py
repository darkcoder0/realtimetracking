from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="index"),
    path('order-pizza/<int:id>',views.Pizzaorder,name="order"),
    path('order-tracking/<str:orderid>/', views.orderTracking, name="order_tracking")
]
