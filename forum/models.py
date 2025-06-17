from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField("Категория", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Topic(models.Model):
    title = models.CharField("Заголовок темы", max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тема"
        verbose_name_plural = "Темы"


class Post(models.Model):
    content = models.TextField("Сообщение")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name="Тема")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Сообщение от {self.author} в теме {self.topic}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Роли пользователей
ROLE_CHOICES = (
    ('student', 'Студент'),
    ('teacher', 'Преподаватель'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    bio = models.TextField("О себе", blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.role}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()