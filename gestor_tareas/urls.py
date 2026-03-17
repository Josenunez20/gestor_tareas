from django.contrib import admin
from django.urls import path, include
from tareas.views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', CustomLoginView.as_view(), name='login'),  # Raíz = login
    path('accounts/', include('django.contrib.auth.urls')),  # logout, password change, etc.
    path('tareas/', include('tareas.urls')),            # todas las URLs de tareas bajo /tareas/
]