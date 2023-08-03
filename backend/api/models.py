from django.db import models
from django.db.models import UniqueConstraint
from users.models import CustomUser


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True,
                            verbose_name='Название')
    color = models.CharField(max_length=10, verbose_name='Цвет')
    slug = models.SlugField(unique=True, verbose_name='Slug')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=255, db_index=True,
                            verbose_name='Название')
    measurement_unit = models.CharField(max_length=10, default='g',
                                        verbose_name='Единицы измерения')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               verbose_name='Автор', related_name='recipes')
    name = models.CharField(max_length=255, verbose_name='Название')
    image = models.ImageField(upload_to='recipes/images/',
                              verbose_name='Изображение')
    text = models.TextField(blank=True, verbose_name='Описание')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipeIngredient',
                                         verbose_name='Ингредиенты')
    tags = models.ManyToManyField(Tag, verbose_name='Теги')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата создания')

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   verbose_name='Ингредиент',
                                   related_name='recipe_ingredients')
    amount = models.PositiveSmallIntegerField(verbose_name='Количество')

    class Meta:
        ordering = ('-id', )
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'
        constraints = [
            UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='recipe_ingredient_unique'
            )
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             related_name='shopping_cart')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               default=None, verbose_name='Рецепт')

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='user_shoppingcart_unique'
            )
        ]


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             related_name='favorite_recipes')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='Рецепт')

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='user_favorite_unique'
            )
        ]
