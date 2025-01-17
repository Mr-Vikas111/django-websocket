from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
import json
from .models import Group, Chat


"""# Sync Consumer"""
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
        
        data = json.loads(event['text'])
        
       
        
        print("user->",self.scope['user'])  
        data['user'] = self.scope['user'].username      
        
        if self.scope['user'].is_authenticated:
            
            # get group name
            group = Group.objects.get(name=self.group_name)
            # create chat
            chat = Chat.objects.create(group=group,content=data['msg'])
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type':'chat.message', # custom handler
                    'message':json.dumps(data) # convert python dict to str
                    
                    
                }
                )
        else:
            self.send({'type':'websocket.send','text':json.dumps({"msg":"login required","user":"Guest"})})
        
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


""" # Async Consumer Class """
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
        data = json.loads(event['text'])
        
        data['user'] = self.scope['user'].username  
        
        # get group name
        if self.scope['user'].is_authenticated:
            group = await database_sync_to_async(Group.objects.get)(name=self.group_name)
            
            # create chat
            await database_sync_to_async(Chat.objects.create)(group=group,content=data['msg'])
            
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type':'chat.message', # custom handler
                    'message':json.dumps(data)
                }
                )
        else:
            await self.send({'type':'websocket.send','text':json.dumps({"msg":"login required","user":"Guest"})})
    
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
    

    
