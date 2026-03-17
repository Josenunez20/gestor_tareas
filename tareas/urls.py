from django.urls import path
from . import views

app_name = 'tareas'

urlpatterns = [
    path('', views.TareaListView.as_view(), name='tarea_list'),
    path('nueva/', views.TareaCreateView.as_view(), name='tarea_create'),
    path('editar/<int:pk>/', views.TareaUpdateView.as_view(), name='tarea_update'),
    path('eliminar/<int:pk>/', views.TareaDeleteView.as_view(), name='tarea_delete'),
    path('marcar/<int:pk>/', views.marcar_completada, name='marcar_completada'),
    path('register/', views.register, name='register'),
]