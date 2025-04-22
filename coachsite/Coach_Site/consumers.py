# Coach_Site/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from asgiref.sync import sync_to_async
from .models import Chat, Message  # Import моделей
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["chat_id"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json.get("type") == "get_history":
            # Загрузка предыдущих сообщений по запросу
            await self.send_previous_messages()
        else:
            message_text = text_data_json["message"]
            user = self.scope["user"]

            if user.is_authenticated:
                user_name = await self.get_username(user)
                # Сохранение сообщения в базу данных
                await self.save_message(user, message_text)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "chat_message",
                        "message": message_text,
                        "user": user_name,
                        "timestamp": str(timezone.now()),
                    },
                )
            else:
                print("Не аутентифицирован")
                pass

    async def chat_message(self, event):
        message = event["message"]
        user = event["user"]
        timestamp = event["timestamp"]
        await self.send(
            text_data=json.dumps(
                {"message": message, "user": user, "timestamp": timestamp}
            )
        )

    async def save_message(self, user, message_text):
        try:
            chat = await self.get_chat()
            await self.create_message(chat, user, message_text)
        except ObjectDoesNotExist:
            print("Чат не найден")

    async def get_previous_messages(self):
        try:
            chat = await self.get_chat()
            messages = await self.get_messages_for_chat(chat)
            return messages
        except ObjectDoesNotExist:
            print("Чат не найден")
            return []

    async def send_previous_messages(self):
        messages = await self.get_previous_messages()
        for message in messages:
            await self.send(
                text_data=json.dumps(
                    {
                        "message": message["text"],
                        "user": message["user"],
                        "timestamp": str(message["timestamp"]),
                    }
                )
            )

    @sync_to_async
    def get_chat(self):
        return Chat.objects.get(id=int(self.room_name))

    @sync_to_async
    def create_message(self, chat, user, message_text):
        Message.objects.create(chat=chat, sender=user, text=message_text)

    @sync_to_async
    def get_messages_for_chat(self, chat):
        messages = []
        for message in Message.objects.filter(chat=chat).order_by("timestamp"):
            messages.append(
                {
                    "text": message.text,
                    "user": message.sender.username,
                    "timestamp": message.timestamp,
                }
            )
        return messages

    @sync_to_async
    def get_username(self, user):
        return user.username
