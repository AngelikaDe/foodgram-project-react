# Generated by Django 3.2.3 on 2023-07-21 22:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='description',
            new_name='text',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='is_favorited',
        ),
        migrations.AddField(
            model_name='recipe',
            name='is_favorited',
            field=models.ManyToManyField(related_name='favorite_recipes', to=settings.AUTH_USER_MODEL),
        ),
    ]