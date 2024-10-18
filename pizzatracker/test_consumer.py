from channels.generic.websocket import WebsocketConsumer
from .models import Pizza,Order
from asgiref.sync import async_to_sync
import json


class OrderPrograss(WebsocketConsumer):
    def connect(self , **kwargs):
        self.room_name = 'main-room'
        self.group_name = 'main-room'
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()
        self.send(text_data = json.dumps({
            "message":"Connection Made"
        }))

        # return super().connect()
   
    # def connect(self):
    #     self.room_name = self.scope['url_route']['kwargs']['order_id']
    #     self.room_group_name = f'order_{self.room_name}'
    #     async_to_sync(self.channel_layer.group_add)(
    #         self.room_group_name,
    #         self.room_name
    #     )
    #     self.accept()
    #     self.send(text_data =json.dumps({
    #         "payload": "Order Details"
    #     }))
    #     return super().connect()


    def receive(self,text_data= None):
        print(text_data)



    def disconnect(self,close_code):
        print(close_code)
