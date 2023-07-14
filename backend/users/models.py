from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(
        'email address',
        max_length=254,
        unique=True,
    )
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]
    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

# class FavoriteRecipe(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

# class ShoppingList(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
