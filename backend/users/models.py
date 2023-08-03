from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Юзернейм'
    )
    first_name = models.CharField(
        max_length=255,
        null=True,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=255,
        null=True,
        verbose_name='Фамилия'
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Почта'
    )
    follow = models.ManyToManyField(
        'self',
        related_name='followers',
        symmetrical=False,
    )
    is_subscribed = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ('username',)

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='Автор',
    )

    class Meta:
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author',),
                name='unique_follow',
            ),
        ]

        def __str__(self):
            return f'Пользователь {self.user} подписался на {self.author}'
