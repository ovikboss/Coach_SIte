from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Coach, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=Coach)
def update_user_is_coach(sender, instance, created, **kwargs):
    if created:
        user = instance.user  # Предполагается, что у Coach есть поле user
        user.is_coach = True
        user.save()

@receiver(post_delete, sender=Coach) # Добавляем сигнал для удаления
def update_user_is_coach_delete(sender, instance, **kwargs):
    user = instance.user  # Предполагается, что у Coach есть поле user
    user.is_coach = False
    user.save()


@receiver(post_save, sender=Comment)
def update_coach_rating_on_comment_save(sender, instance, **kwargs):
    if instance.coach:
        print(
            f"Обновляем рейтинг тренера {instance.coach.user.username} после сохранения комментария")  # Отладочный вывод
        instance.coach.update_rating()
    else:
        print("Внимание: У комментария нет тренера!")  # Отладочный вывод
@receiver(post_delete, sender=Comment)
def update_coach_rating_on_comment_delete(sender, instance, **kwargs):
    """Обновляет рейтинг тренера при удалении комментария."""
    if instance.coach:
        print(f"Обновляем рейтинг тренера {instance.coach.user.username} после удаления комментария")  # Отладочный вывод
        instance.coach.update_rating()
    else:
        print("Внимание: У комментария нет тренера!")