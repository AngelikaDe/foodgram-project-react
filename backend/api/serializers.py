from rest_framework import serializers
from .models import Recipe, Tag
from django.contrib.auth import get_user_model
from rest_framework.serializers import (ModelSerializer, SerializerMethodField,
                                        ValidationError)
from drf_extra_fields.fields import Base64ImageField
from users.models import CustomUser
from djoser.serializers import UserCreateSerializer, UserSerializer


User = get_user_model()

class CustomUserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'password',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_is_subscribed(self, author):
        user = self.context.get('request').user
        if user.is_anonymous or (user == author):
            return False
        return user.follow.filter(id=author.id).exists()

class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'email', 'username', 'first_name',
            'last_name', 'password')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']

class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)

    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'

# class UserSubscribeSerializer(UserSerializer):
#     """Сериализатор вывода авторов на которых подписан текущий пользователь.
#     """
#     recipes = SerializerMethodField(read_only=True)
#     recipes_count = SerializerMethodField()

#     class Meta:
#         model = User
#         fields = (
#             'email',
#             'id',
#             'username',
#             'first_name',
#             'last_name',
#             'is_subscribed',
#             'recipes',
#             'recipes_count',
#         )
#         read_only_fields = '__all__',

#     def get_is_subscribed(*args):
#         """Проверка подписки пользователей.
#         Переопределённый метод родительского класса для уменьшения нагрузки,
#         так как в текущей реализации всегда вернёт `True`.
#         """
#         return True

#     def get_recipes_count(self, author):
#         """Показывает общее количество рецептов у каждого автора author."""
#         return author.recipes.count()

#     def get_recipes(self, obj):
#         """Показывает рецепты авторов в подписках"""
#         request = self.context.get('request')
#         recipes = obj.recipes.all()
#         limit = request.query_params.get('recipes_limit')
#         if limit:
#             recipes = recipes[:int(limit)]
#         return RecipeSerializer(recipes, many=True).data