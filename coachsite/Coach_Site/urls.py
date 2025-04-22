from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("my_profile/", views.my_profile, name="my_profile"),
    path("coach/<int:coach_id>/", views.coach_detail, name="coach_detail"),
    path("add_comment/<int:coach_id>", views.add_comment, name="add_comment"),
    path("my_profile_comments/", views.user_comments, name="user_comments"),
    path("edit_comment/<int:comment_id>/", views.edit_comment, name="edit_comment"),
    path("profile/", views.edit_profile, name="edit_profile"),
    path("register_as_coach/", views.register_as_coach, name="register_as_coach"),
    path("register/", views.register, name="register"),
    path("chat/start/<int:coach_id>/", views.start_chat, name="start_chat"),
    path("chat/<int:chat_id>/", views.chat_detail, name="chat_detail"),
    path("chats/", views.chat_list, name="chat_list"),  # Добавляем URL для списка чатов
    path("coach/schedule/", views.coach_schedule, name="coach_schedule"),
    path("book/<int:slot_id>/", views.book_training, name="book_training"),
    path("user/schedule/", views.user_schedule, name="user_schedule"),
    path(
        "coach/requests/", views.coach_training_requests, name="coach_training_requests"
    ),
    path("confirm/<int:session_id>/", views.confirm_training, name="confirm_training"),
    path("reject/<int:session_id>/", views.reject_training, name="reject_training"),
]
