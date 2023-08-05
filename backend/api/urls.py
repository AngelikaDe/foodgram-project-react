from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import CustomUserViewSet

from api.views import TagViewSet, RecipeViewSet, IngredientViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'tags', TagViewSet, 'tags')
router.register(r'ingredients', IngredientViewSet, 'ingredients')
router.register(r'recipes', RecipeViewSet, 'recipes')
router.register(r'users', CustomUserViewSet, 'users')

urlpatterns = (
    path('', include(router.urls)),
)
