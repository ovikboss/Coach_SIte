from email.policy import default

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator



class Coach(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    bio = models.TextField(blank=True)
    experience_years = models.IntegerField(default=0, verbose_name="Стаж (лет)")
    rating = models.FloatField(default=0.0, verbose_name="Рейтинг")
    hide_phone_number = models.BooleanField(default=False, verbose_name='Скрыть номер телефона')

    def __str__(self):
        return self.user.username

    def update_rating(self):
        """Пересчитывает рейтинг тренера на основе связанных комментариев."""
        comments = self.comment_set.all()
        if comments:
            total_rating = sum(comment.raiting for comment in comments)
            self.rating = round(total_rating / comments.count(),2)
        else:
            self.rating = 0.0  # Если нет комментариев, рейтинг = 0
        self.save()


class Comment(models.Model):
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, verbose_name='Тренер')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')
    text = models.TextField(verbose_name='Текст комментария')
    raiting = models.IntegerField(default=1, verbose_name='Рейтинг',
                                   validators=[MaxValueValidator(5), MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Комментарий от {self.author.username} к {self.coach.user.username}'

class Chat(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='chats_as_user', on_delete=models.CASCADE)
    coach = models.ForeignKey('Coach_Site.Coach', related_name='chats_as_coach', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Чат между {self.user.username} и {self.coach.user.username}'

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Сообщение от {self.sender.username} в {self.chat}'

    class Meta:
        ordering = ['timestamp'] # Сортируем сообщения по времени

class AvailableSlot(models.Model):
    coach = models.ForeignKey('Coach_Site.Coach', on_delete=models.CASCADE, related_name='available_slots')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.coach.user.username}: {self.start_time} - {self.end_time}"

    def overlaps_with_training_session(self):
        """Проверяет, пересекается ли слот с какой-либо тренировкой."""


        # Проверяем, есть ли тренировки, которые начинаются или заканчиваются внутри этого слота
        return TrainingSession.objects.filter(
            coach=self.coach,  # Убедитесь, что тренировка с тем же тренером
            slot__start_time__lt=self.end_time,  # ИСПОЛЬЗУЕМ slot__start_time
            slot__end_time__gt=self.start_time  # ИСПОЛЬЗУЕМ slot__end_time
        ).exists()

class TrainingSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='training_sessions')
    coach = models.ForeignKey('Coach_Site.Coach', on_delete=models.CASCADE, related_name='training_sessions')
    slot = models.ForeignKey(AvailableSlot, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Ожидает подтверждения'),
            ('confirmed', 'Подтверждено'),
            ('rejected', 'Отклонено'),
        ],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Тренировка {self.user.username} с {self.coach.user.username} ({self.slot.start_time})"