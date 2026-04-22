import firebase_admin
from firebase_admin import credentials, messaging
import os

# Инициализация (сделай это один раз при запуске приложения)
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

def send_push_notification(tokens: list, title: str, body: str):
    if not tokens:
        return
    
    # Создаем сообщение
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        tokens=tokens,
    )
    
    # Отправляем
    response = messaging.send_each_for_multicast(message)
    print(f"Успешно отправлено: {response.success_count}")