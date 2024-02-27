# your_project_name/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('joblink/', include('joblink.urls')),  # Include your app's URLs
]
