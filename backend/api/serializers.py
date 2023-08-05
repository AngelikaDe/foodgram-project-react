import re
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from users.models import CustomUser, Follow
from djoser.serializers import UserCreateSerializer, UserSerializer

from .models import (
    Recipe,
    Tag,
    ShoppingCart,
    Ingredient,
    RecipeIngredient,
    FavoriteRecipe
)

MIN_COOKING_TIME = 1
MAX_COOKING_TIME = 32000


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'email', 'username', 'first_name',
            'last_name', 'password')

    def validate_username(self, value):
        if not re.match(r'^[\w.@+-]+$', value):
            raise serializers.ValidationError('Недопустимые символы.')
        return value


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'is_subscribed']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_is_subscribed(self, author):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        if user == author:
            return True
        return user.follow.filter(id=author.id).exists()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class RecipeIngredientSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(source='ingredient.id')
    amount = serializers.IntegerField(min_value=MIN_COOKING_TIME,
                                      max_value=MAX_COOKING_TIME,
                                      error_messages={
                                          'min_value': ('Значение должно быть'
                                                        'больше или равно'
                                                        '{min_value}.'),
                                          'max_value': ('Значение должно быть'
                                                        'меньше или равно'
                                                        '{max_value}.')})

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):

    image = Base64ImageField()
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(
        many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            'id',
            'name',
            'image',
            'cooking_time',
            'tags',
            'author',
            'is_in_shopping_cart',
            'is_favorited',
            'ingredients',
            'text']

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return obj in user.favorite_recipes.all()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return obj in user.shopping_cart.all()

    def create(self, validated_data):
        ingredients = self.initial_data.get('ingredients', [])
        tags_data = self.context['request'].data.get('tags', [])
        recipe = Recipe.objects.create(
            author=self.context['request'].user,
            name=validated_data['name'],
            image=validated_data['image'],
            cooking_time=validated_data['cooking_time'],
            text=validated_data['text']
        )
        recipe_ingredients = [
            RecipeIngredient(
                recipe=recipe,
                ingredient_id=ingredient['id'],
                amount=ingredient['amount']
            )
            for ingredient in ingredients
        ]
        RecipeIngredient.objects.bulk_create(recipe_ingredients)
        recipe.tags.add(*tags_data)

        return recipe

    def to_representation(self, instance):
        data = super().to_representation(instance)
        ingredients_data = instance.ingredients.all()
        data['ingredients'] = RecipeIngredientSerializer(
            ingredients_data, many=True).data
        return data


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']


class ShoppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe',)


class FollowSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = '__all__',
        read_only_fields = '__all__',

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def create(self, validated_data):
        request = self.context.get('request', None)
        author_id = self.context.get('request').parser_context.get(
            'kwargs').get('user_id')
        current_user = request.user
        author = get_object_or_404(CustomUser, pk=author_id)
        Follow.objects.create(user=current_user, author=author)
        return author


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteRecipe
        fields = '__all__'
