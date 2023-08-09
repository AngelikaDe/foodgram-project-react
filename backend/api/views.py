from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import (
    Recipe,
    Tag,
    ShoppingCart,
    Ingredient,
    FavoriteRecipe,
)

from .permissions import OnlyAuthorOrStaff
from .serializers import (
    TagSerializer,
    ShoppingCartSerializer,
    IngredientSerializer,
    RecipeCreateSerializer,
    FavoriteRecipeSerializer,
    RecipeSerializer,
)

from users.pagination import CustomUserPagination


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, ]
    pagination = CustomUserPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    @action(detail=True,
            methods=['post',
                     'delete'],
            permission_classes=[OnlyAuthorOrStaff],
            url_path='shopping_cart')
    def shopping_cart(self, request, pk=None):
        shopping_cart = {'request': request}
        recipe = get_object_or_404(Recipe, id=pk)

        if request.method == 'POST':
            serializer = ShoppingCartSerializer(data={
                'user': request.user.id,
                'recipe': recipe.id
            }, context=shopping_cart)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response_serializer = RecipeSerializer(
                recipe, context={'request': request})
            return Response(response_serializer.data,
                            status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            user = request.user
            favorites = get_object_or_404(
                ShoppingCart, user=user, recipe=recipe
            )
            favorites.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], permission_classes=[
            IsAuthenticated], url_path='download_shopping_cart')
    def download(self, request):
        shopping_cart = ShoppingCart.objects.filter(user=request.user)
        file_content = 'Cписок покупок:\n'

        for item in shopping_cart:
            recipe = item.recipe
            file_content += f"Recipe: {recipe.name}\n"

            ingredients = recipe.recipe_ingredients.all()
            for ingredient in ingredients:
                amount = ingredient.amount
                ingredient_name = ingredient.ingredient.name
                measurement_unit = ingredient.ingredient.measurement_unit
                file_content += (
                    f"\n{ingredient_name} - "
                    f"{amount} {measurement_unit}")
            file_content += "\n"

        response = Response(file_content, content_type='text/plain')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_cart.txt"')
        return response

    @action(detail=True, permission_classes=[IsAuthenticated],
            methods=['post', 'delete'], url_path='favorite')
    def favorite_unfavorite_recipe(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            data = {
                'user': user.id,
                'recipe': recipe.id,
            }
            serializer = FavoriteRecipeSerializer(
                data=data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        elif request.method == 'DELETE':
            favorite_recipe = get_object_or_404(
                FavoriteRecipe, user=user, recipe=recipe
            )
            favorite_recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = RecipeCreateSerializer(
            recipe, context={'request': request})
        response_data = {
            'id': serializer.data['id'],
            'name': serializer.data['name'],
            'image': serializer.data['image'],
            'cooking_time': serializer.data['cooking_time'],
        }
        return Response(response_data)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
