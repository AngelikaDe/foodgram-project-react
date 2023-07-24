from django.shortcuts import render
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import Recipe, Tag, ShoppingCart
from users.models import Follow
from rest_framework.response import Response
from rest_framework.decorators import action
# from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import RecipeSerializer, TagSerializer, ShoppingCartSerializer, RecipeDetailSerializer, FollowSerializer
from users.pagination import CustomUserPagination

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # permission_classes = (IsAdminOrReadOnly,)

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = CustomUserPagination

    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def create_recipe(request):
        print("STILL\n\n\n\n")
        data = request.data
        data['author'] = request.user.id
        serializer = RecipeSerializer(data=data)
        # serializer = RecipeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
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

    @action(detail=True, methods=['post'], url_path='shopping_cart')
    def shopping_cart(self, request, pk=None):
        shopping_cart = {'request': request}
        recipe = get_object_or_404(Recipe, id=pk)
        serializer = ShoppingCartSerializer(data={
            'user': request.user.id,
            'recipe': recipe.id
        }, context=shopping_cart)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def download(self, request):
        shopping_cart = ShoppingCart.objects.get(user=request.user)

        # Here you can implement the logic to generate the download file (TXT/PDF/CSV) based on the shopping cart data.
        # For example, you can use the "reportlab" library for generating PDFs or "csv" module for generating CSV files.

        # For demonstration purposes, let's assume we are returning a simple message in the response.
        return Response({'message': 'Download file generated successfully.'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], url_path='favorite')
    def favorite_recipe(self, request, pk=None):
        recipe = self.get_object()
        user = request.user
        if recipe.is_favorited.filter(pk=user.pk).exists():
            recipe.is_favorited.remove(user)
            is_favorited = False
        else:
            recipe.is_favorited.add(user)
            is_favorited = True
        serializer = RecipeDetailSerializer(recipe, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['delete'], url_path='favorite')
    def unfavorite_recipe(self, request, pk=None):
        recipe = self.get_object()
        user = request.user
        if recipe.is_favorited.filter(pk=user.pk).exists():
            recipe.is_favorited.remove(user)
            return Response(status=200)
        else:
            return Response({'errors': 'Recipe is not in favorites.'}, status=400)
