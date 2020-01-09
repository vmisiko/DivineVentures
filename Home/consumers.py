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
from pinax.referrals.models import Referral,ReferralResponse
from .models import Profile
# from .models import  

class EchoConsumer(AsyncConsumer):
    
    async def websocket_connect(self, event):
        print("connected", event)
       
        # await asyncio.sleep(5)
        user = self.scope["user"]
        EchoConsumer.user = user
        self.user = user
        self.chat_room =f"group-name-{user.username}"
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
        #         "text" : " hellow victor is texting"
        #     }
        # )

    async def websocket_receive(self, event):
        print("received", event)
        await self.send({
            "type": "websocket.send",
            "text": "hello word",
        })
    async def Websocket_disconnect(self, event):
        print("disconnected", event)

    async def send_message(self, event):
        print("message", event)
        await self.send({
            "type": "websocket.send",
            "text":event["text"]
        })
    async def user(self):
        user = self.scope["user"]
        return user


    @staticmethod
    @receiver(signals.post_save, sender = ReferralResponse)
    def send_actual_signal(sender, instance, **kwargs):
        
        referral_code = Profile.objects.get(referral = instance.referral )
        print(referral_code.user, "this is the referral user")
        chat_room =f"group-name-{referral_code.user}"
        qr = ReferralResponse.objects.filter(referral= referral_code.referral, action ="SIGNED_UP"  ).count()
        print(qr, "signed up")

        paid = ReferralResponse.objects.filter(referral = referral_code.referral, action ="PAID"  ).count()

        clicks = ReferralResponse.objects.filter(referral = referral_code.referral, action ="RESPONDED"  ).count()
        channel_layer = channels.layers.get_channel_layer()
        # user = list(referral_code.user)
        user = get_user_model()

        qs = user.objects.get(username = referral_code.user)
        print(qs.username)
        message = {
            "paid": paid,
            "signed_up": qr,
            "clicks": clicks,
            "user":qs.username
        }

        async_to_sync(channel_layer.group_send)(chat_room, {
            "type":"send_message",
            "text": json.dumps(message)
        })

