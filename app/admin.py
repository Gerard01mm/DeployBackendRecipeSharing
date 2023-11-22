# Import necessary modules and classes from Django
from django.contrib import admin
from .models import Recipe


# Define a custom RecipeAdmin class that extends admin.ModelAdmin
class RecipeAdmin(admin.ModelAdmin):
    # Define fieldsets to organize fields in the admin interface
    fieldsets = [
        (None, {'fields': ['title']}),
        (None, {'fields': ['ingredients']}),
        (None, {'fields': ['instructions']}),
        (None, {'fields': ['preparation_time']}),
        (None, {'fields': ['servings']}),
        (None, {'fields': ['kcal']}),
        (None, {'fields': ['username_id']}),
        (None, {'fields': ['creation_date']}),
        (None, {'fields': ['recipe_type']}),
        (None, {'fields': ['allergens']})
    ]

    # Define the list_display property to specify
    # which fields are displayed in the list view
    list_display = (
        'title',
        'ingredients',
        'instructions',
        'preparation_time',
        'servings',
        'kcal',
        'username_id',
        'creation_date',
        'recipe_type',
        'allergens'
    )


# Register the Recipe model with the custom RecipeAdmin class
# in the admin site
admin.site.register(Recipe, RecipeAdmin)
