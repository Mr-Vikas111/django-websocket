# from channels.consumer import SyncConsumer, AsyncConsumer
# from channels.exceptions import StopConsumer
# from time import sleep

# # SyncConsumer
# class MySyncConsumer(SyncConsumer):
    
#     def websocket_connect(self,event):
#         print("websocket connect")
#         self.send({
#             'type':'websocket.accept'
#         })
        
#     def websocket_receive(self,event):
#         print("websocket receive",event)
#         print("websocket receive text",event['text'])
        
#         for i in range(10):
#             # send msg to client function
#             self.send({
#                 'type':'websocket.send',
#                 'text':str(i)
#             })
#             sleep(1)
            
#     def websocket_disconnect(self,event):
#         print("websocket disconnect")
#         raise StopConsumer()
        
        
# # AsyncConsumer
# class MyAsyncConsumer(AsyncConsumer):
    
#     async def websocket_connect(self,event):
#         print("websocket connect")
#         await self.send({
#             'type':'websocket.accept'
#         })
        
#     async def websocket_receive(self,event):
#         print("websocket receive")
        
#         # send msg to client
#         await self.send({
#             'type':'websocket.send',
#             'text':"mai hu server"
#         })
        
        
#     async def websocket_disconnect(self,event):
#         print("websocket disconnect")
#         raise StopConsumer()



from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync



class MySyncConsumer(SyncConsumer):
    def websocket_connect(self,event):
        print("websocket connect",event)
        
        print("Channel Layer ..",self.channel_layer) # get default channel layer

        print("Channel Name ..",self.channel_name) # get default channel name
        
        self.group_name = self.scope['url_route']['kwargs']['groupname']
        
        print("group name ->",self.group_name)
        
        # add channels in a new or existing group (note -> group_add() is async function) and it must be
        # convert to sync function that's way we use async_to_sync function
        async_to_sync(self.channel_layer.group_add)(
            self.group_name, # group name
            self.channel_name
        )
        
        self.send({
            'type':'websocket.accept'
        })
        
    
        
        
    def websocket_receive(self,event):
        print("message receive from client",event)
        
        print("message fro client side ",event['text'])
        
        print("type of message ->",type(event['text']))
        
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type':'chat.message', # custom handler
                'message':event['text']
            }
            )
    
    # create custom handler for send message to client 
    def chat_message(self,event):
        print("event .. of chat message ->",event['message'])
        print("event .. of chat message ->",type(event['message']))
        
        self.send({
            'type':'websocket.send',
            'text':event['message']
        })
        
        
    
    def websocket_disconnect(self,event):
        print("websocket disconnected",event)
        
        print("Channel Layer ..",self.channel_layer) # get default channel layer

        print("Channel Name ..",self.channel_name) # get default channel name
        
        # discard group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )
        raise StopConsumer


class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print("websocket connect",event)
        
        print("Channel Layer ..",self.channel_layer) # get default channel layer

        print("Channel Name ..",self.channel_name) # get default channel name
        
        self.group_name = self.scope['url_route']['kwargs']['groupname']
        
        await self.channel_layer.group_add(
            self.group_name, # group name
            self.channel_name
        )
        
        await self.send({
            'type':'websocket.accept'
        })
        
    
        
        
    async def websocket_receive(self,event):
        print("message receive from client",event)
        
        print("message fro client side ",event['text'])
        
        print("type of message ->",type(event['text']))
        
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type':'chat.message', # custom handler
                'message':event['text']
            }
            )
    
    # create custom handler for send message to client 
    async def chat_message(self,event):
        print("event .. of chat message ->",event['message'])
        print("event .. of chat message ->",type(event['message']))
        
        await self.send({
            'type':'websocket.send',
            'text':event['message']
        })
        
        
    
    async def websocket_disconnect(self,event):
        print("websocket disconnected",event)
        
        print("Channel Layer ..",self.channel_layer) # get default channel layer

        print("Channel Name ..",self.channel_name) # get default channel name
        
        # discard group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        raise StopConsumer
    

    
