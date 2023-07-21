from rest_framework import serializers
from .models import Recipe, Tag, ShoppingCart
from django.contrib.auth import get_user_model
from rest_framework.serializers import (ModelSerializer, SerializerMethodField,
                                        ValidationError)
from drf_extra_fields.fields import Base64ImageField
from users.models import CustomUser, Follow
from djoser.serializers import UserCreateSerializer, UserSerializer


User = get_user_model()
class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'email', 'username', 'first_name',
            'last_name', 'password')
    def validate_username(self, value):
        print("paботает \n \n \n\n")
        # username = value
        # if not re.match(r'^[\w.@+-]+\z',username):
        #     ValidationError(
        #         "Недопустимые символы"
        #     )
        return value

class CustomUserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField(read_only=True)

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

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']

class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)
    # is_favorited = serializers.SerializerMethodField()
    # is_in_shopping_cart = serializers.SerializerMethodField()

    # def get_is_favorited(self, obj):
    #     # Implement your logic to determine if the recipe is favorited
    #     # For example, you can check if the recipe is in the user's favorites
    #     # and return True or False accordingly.
    #     user = self.context['request'].user
    #     return obj.is_favorited_by_user(user)  #
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time', 'tags', 'author']

    # def is_favorited(self, recipe):
    #     return recipe.is_favorited.count()

class RecipeDetailSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']

class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe',)
    
class FollowSerializer(UserSerializer):
    recipes = SerializerMethodField(read_only=True)
    recipes_count = SerializerMethodField()

    class Meta:
        model = Follow
        fields = '__all__',
        # (
        #     'email',
        #     'id',
        #     'username',
        #     'first_name',
        #     'last_name',
        #     'is_subscribed',
        #     'recipes',
        #     'recipes_count',
        # )
        read_only_fields = '__all__',

    # def get_is_subscribed(*args):
    #     return True

    # def get_recipes_count(self, author):
    #     return author.recipes.count()

    # def get_recipes(self, obj):
    #     request = self.context.get('request')
    #     recipes = obj.recipes.all()
    #     limit = request.query_params.get('recipes_limit')
    #     if limit:
    #         recipes = recipes[:int(limit)]
    #     return RecipeSerializer(recipes, many=True).data
