from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Tarea(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tareas')
    descripcion = models.CharField(max_length=200, verbose_name="Descripción")
    completada = models.BooleanField(default=False, verbose_name="Completada")
    fecha_vencimiento = models.DateField(null=True, blank=True, verbose_name="Fecha de vencimiento")
    creada = models.DateTimeField(auto_now_add=True, verbose_name="Creada")

    class Meta:
        ordering = ['-creada']

    def __str__(self):
        return self.descripcion

    def esta_vencida(self):
        """Retorna True si la tarea no está completada y su fecha de vencimiento ya pasó."""
        if not self.completada and self.fecha_vencimiento and self.fecha_vencimiento < timezone.now().date():
            return True
        return False