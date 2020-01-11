import asyncio
import json
from django.contrib.auth import get_user_model
# from django.contrib.auth import User

from asgiref.sync import async_to_sync
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
import channels.layers
from django.db.models import signals
from django.dispatch import receiver
# from pinax.referrals.models import Referral,ReferralResponse
from Home.models import Profile
from .models import  LNMOnline

class ConfirmMpesaPayment(AsyncConsumer):
    
    async def websocket_connect(self, event):
        print("connected", event)
        self.chat_room ='group-send-chat-room'
        await self.channel_layer.group_add(
            self.chat_room, 
            self.channel_name
        )
      
        await self.send({

            "type": "websocket.accept",  
        })

        
        # await self.channel_layer.group_send(
        #     self.chat_room,
        #     {
        #         "type": "send_message",
        #         "message" : json.dumps(message)
        #     }
        # )

    async def websocket_receive(self, event):
        print("received", event)
        front_end = event.get("text", None)
        if front_end is not None:
            data = json.loads(front_end)
            user = data.get('user')
            await self.send({

            "type": "websocket.send", 
            "text": f"imekubali {user}" 
        })

            profile = Profile.objects.get(user__username = user, paid = False)
            print(profile, "checking if profile is not none")
            profile.paid = True
            profile.save()

           
            
            

    async def send_message(self, event):
        print("it sending")
        await self.send({
            "type": "websocket.send",
            "text": event['text'],
        })
    async def Websocket_disconnect(self, event):
        print("disconnected", event)

    @staticmethod
    @receiver(signals.post_save, sender = LNMOnline)
    def send_actual_signal(sender, instance, **kwargs):
        
        phone_number = instance.PhoneNumber
        amount = instance.Amount
        channel_layer = channels.layers.get_channel_layer()
        # user = list(referral_code.user)
        user = get_user_model()
        chat_room ='group-send-chat-room'
        message = {
            "phone_number": phone_number,
            "amount": amount,
        }

        async_to_sync(channel_layer.group_send)(chat_room, {
            "type":"send_message",
            "text": json.dumps(message)
        })

 