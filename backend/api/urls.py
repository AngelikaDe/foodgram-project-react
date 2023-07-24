from django.urls import include, path
from rest_framework.routers import DefaultRouter

# from .views import IngredientViewSet, RecipeViewSet, TagViewSet
from users.views import CustomUserViewSet
from .views import TagViewSet, RecipeViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'tags', TagViewSet, 'tags')
# router.register('ingredients', IngredientViewSet, 'ingredients')
router.register(r'recipes', RecipeViewSet, 'recipes')
router.register(r'users', CustomUserViewSet, 'users')

urlpatterns = (
    path('', include(router.urls)),
)
