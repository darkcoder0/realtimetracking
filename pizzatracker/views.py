from django.shortcuts import render,redirect

from django.contrib import messages
from . models import  Order,Pizza
# Create your views here.


def home(request):
    pizza = Pizza.objects.all()
    order = Order.objects.all()

    return render(request,'pizzatracker/index.html',context = {'pizzas':pizza,'orders':order})


def orderTracking(request,orderid):
    order_detail = Order.objects.get(pk=orderid)
    return render(request,'pizzatracker/orderstatus.html',context = {'order':order_detail})


def Pizzaorder(request,id):
    pizza = Pizza.objects.get(id=id)
    Order.objects.create(
        pizza = pizza,
        user = request.user,
        amount = pizza.price
    )
    messages.add_message(request, messages.INFO, "Order Placed")
    return redirect('/')