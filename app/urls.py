from django.urls import path, include
from app.views import *

app_name = 'app'
urlpatterns = [
    path('', HomeView.as_view(), name='homepage'),
    path('register/', RegisterView.as_view(), name='registerpage'),
    path('login/', LoginView.as_view(), name='loginpage'),
    path('addRecipe/', AddRecipeView.as_view(), name='addRecipe'),
    path('recipes/<str:query>/', QueryListRecipes.as_view(), name='queryListRecipes'),
    path('recipesPostRatings/', RecipeView.as_view(), name='postRatingRecipe'),
    path('recipesAddFavorites/', PostFavoriteRecipe.as_view(), name='addRecipeToFavorite'),
    path('recipes/getratings/<str:query>/', GetRatingsByID.as_view(), name='getRatingRecipe'),
    path('user/<str:username>/', GetUserByUsername.as_view(), name='getUser'),
    path('recipe/<str:recipe_id>/', RecipeView.as_view(), name='recipe'),
]

urlpatterns += [
    path('login/', include('django.contrib.auth.urls')),
]
