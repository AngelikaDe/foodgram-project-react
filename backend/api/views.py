from django.shortcuts import render
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import Recipe, Tag
# from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import RecipeSerializer, TagSerializer
from users.pagination import CustomUserPagination

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # permission_classes = (IsAdminOrReadOnly,)

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = CustomUserPagination
    
    @api_view(['GET'])
    def recipe_list(request):
        is_favorited = request.query_params.get('is_favorited')
        is_in_shopping_cart = request.query_params.get('is_in_shopping_cart')
        author_id = request.query_params.get('author')
        tags = request.query_params.getlist('tags')
        limit = request.query_params.get('limit', 10)

        recipes = Recipe.objects.all()

        if is_favorited:
            recipes = recipes.filter(is_favorited=is_favorited)
        if is_in_shopping_cart:
            recipes = recipes.filter(is_in_shopping_cart=is_in_shopping_cart)
        if author_id:
            recipes = recipes.filter(author_id=author_id)
        if tags:
            recipes = recipes.filter(tags__slug__in=tags)

        paginator = PageNumberPagination()
        paginator.page_size = limit
        paginated_recipes = paginator.paginate_queryset(recipes, request)

        serializer = RecipeSerializer(paginated_recipes, many=True)
        return paginator.get_paginated_response(serializer.data)


    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def create_recipe(request):
        serializer = RecipeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(author=request.user)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


    @api_view(['GET'])
    def get_recipe(request, id):
        recipe = get_object_or_404(Recipe, id=id)
        serializer = RecipeSerializer(recipe)
        return JsonResponse(serializer.data)


    @api_view(['PUT'])
    @permission_classes([IsAuthenticated])
    def update_recipe(request, id):
        recipe = get_object_or_404(Recipe, id=id)

        if recipe.author != request.user:
            return JsonResponse({'detail': 'У вас нет разрешения на редактирование этого рецепта.'}, status=403)

        serializer = RecipeSerializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)


    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated])
    def delete_recipe(request, id):
        recipe = get_object_or_404(Recipe, id=id)

        if recipe.author != request.user:
            return JsonResponse({'detail': 'У вас нет разрешения на удаление этого рецепта.'}, status=403)

        recipe.delete()
        return JsonResponse({'detail': 'Рецепт успешно удален.'})
