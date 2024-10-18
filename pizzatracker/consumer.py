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



