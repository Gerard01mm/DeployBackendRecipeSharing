# Import the necessary modules and classes for URL configuration
from django.contrib import admin
from django.urls import path, include

# Define URL patterns for the project
urlpatterns = [
    # Define a URL pattern for the admin site
    path('admin/', admin.site.urls),

    # Include URL patterns from the 'app' application
    # (referenced via its 'urls.py')
    path('', include("app.urls")),
]

# Include URL patterns for built-in authentication views
urlpatterns += [
    path('admin/', include('django.contrib.auth.urls')),
]
