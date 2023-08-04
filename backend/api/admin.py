from django.contrib import admin
from .models import (Tag, Ingredient,
                     Recipe, RecipeIngredient,
                     ShoppingCart, FavoriteRecipe)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'total_favorites')
    list_filter = ('name', 'author', 'tags')
    search_fields = ('name', 'author__username', 'tags__name')

    def total_favorites(self, obj):
        return obj.shoppingcart_set.count()
    total_favorites.short_description = 'Favorites Count'


class IngredientAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    search_fields = ('name',)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'recipe']
    search_fields = ['user__username', 'user__email']


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
admin.site.register(RecipeIngredient)
admin.site.register(ShoppingCart)
admin.site.register(FavoriteRecipe)
