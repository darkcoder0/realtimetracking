import uuid
from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer 
from asgiref.sync import async_to_sync 
import json
# Create your models here.

class Pizza(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField(default=100)
    image = models.URLField(max_length=250)
    desc = models.TextField(max_length=250)

    def __str__(self) -> str:
        return self.name


order_mapper = {
    "Order Recieved" : 15,
    "Baking" : 40,
    "Baked" :60,
    "Out of Delivery" : 80,
    "Order Develivery" : 100 
}

class Order(models.Model):
    STATUS = (("Order Recieved","Order Recieved"),
                ("Baking","Baking"),
                ("Baked","Baked"),
                ("Out of Delivery","Out of Delivery"),
                ("Order Develivery","Order Develivery"))

    pizza = models.ForeignKey(Pizza,on_delete=models.CASCADE)   
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.FloatField()
    status = models.CharField(max_length=100,choices=STATUS, default="Order Recieved")
    created_at = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.pizza} - {self.status}"
    

    @staticmethod
    def give_order_details(order_id):
        instance = Order.objects.get(order_id = order_id)
    
        return {
            "order_id": str(instance.order_id),
            "amount": instance.amount,
            "status": instance.status,
            "order_progress":order_mapper[instance.status]
        }
    


@receiver(post_save, sender = Order)
def order_status_handler(sender,instance,created,**kwargs):
    if not created:
        channel_layer = get_channel_layer()
        data =  {
            "order_id": str(instance.order_id),
            "amount": instance.amount,
            "status": instance.status,
            "order_progress":order_mapper[instance.status]
        }
        async_to_sync(channel_layer.group_send)(
            f'order_{instance.order_id}',
            {
                'type':'order_status',
                'value':json.dumps(data)
            })