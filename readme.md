create dajango project 

then after create app 

then register app in setting.py

create order schema 

create pizz list chema 

create static folder in app directory

create template directory add same app name  add base.html and as per requirement file 

add static and template direcotry in setting.py


install requirend 

use 

channel 
redish 
signal 

create consumer.py file in  (like view.py weite your logic )

cofigure asig file 


"""
ASGI config for realtimetracking project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtimetracking.settings')


application = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from pizzatracker.consumer import OrderProgess



ws_pattern = [
    path("ws/pizza/<order_id>/",OrderProgess),
]

application = ProtocolTypeRouter({
    "websocket": (
        (
            URLRouter(ws_pattern)
        )
    ),
})



set as per route file for websokcket url 




configure setting.py file 

    'channels',  


    add in installed app 


# WSGI_APPLICATION = 'realtimetracking.wsgi.application'
ASGI_APPLICATION = 'realtimetracking.asgi.application'

comment wegi aplicaion
and uncomment asgi apiilication



add channel layer 


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}



add consumenr.py

from channels.generic.websocket import WebsocketConsumer
from .models import Pizza,Order
from asgiref.sync import async_to_sync,sync_to_async
import json


class OrderProgess(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['order_id']
        self.room_group_name = f'order_{self.room_name}' 
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        order = Order.give_order_details(self.room_name)
        # exit()
        self.accept()
        self.send(text_data = json.dumps(
            {
                "payload":order
            }
        ))

        # return super().connect()
    
    # def order_status(self,event):
    #     print(event)
    #     print("hello",event)
    #     data = json.loads(event['value'])
    #     print(data)


    def order_status(self, event):
        # Print event for debugging purposes
        print("Received order status event:", event)
        
        # Parse the data from the event
        data = json.loads(event['value'])
        print("Parsed data:", data)

        # Send the updated order status to the WebSocket client
        self.send(text_data=json.dumps({
            'payload': data
        }))



        
    def receive(self, text_data=None, bytes_data=None):
        pass        

    def disconnect(self, close_code):
        # Remove the WebSocket connection from the group on disconnect
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )






from dajngo challen documention  change as per requiremen llogic 


go to model file to create signal functionlity to when some chancge on order chancge then triggger  signal send to trigger event


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

            add this code to in your djagno model file form trigger whenever change order status


            after then test in websocket king 
            add url add order id  hit enter 

            return json payload then after send to template file 
    



and finally step to add websoket url in templfile call and update in document.getelemt id  through update ui 



change order status  work or not 



then after install tailwind css installl



