from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.utils import timezone
from .models import Tarea
from .forms import TareaForm

# Vista personalizada para el login (raíz)
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

# Registro de usuarios
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Cuenta creada para {username}. ¡Ya puedes iniciar sesión!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

class TareaListView(LoginRequiredMixin, ListView):
    model = Tarea
    context_object_name = 'tareas'
    template_name = 'tareas/tarea_list.html'

    def get_queryset(self):
        tareas = Tarea.objects.filter(usuario=self.request.user)
        
        # Cancelar automáticamente las tareas vencidas
        for tarea in tareas:
            if tarea.esta_vencida() and not tarea.cancelada:
                tarea.cancelada = True
                tarea.save()
        
        return tareas

class TareaCreateView(LoginRequiredMixin, CreateView):
    model = Tarea
    form_class = TareaForm
    success_url = reverse_lazy('tareas:tarea_list')
    template_name = 'tareas/tarea_form.html'

    def form_valid(self, form):
        # Validar que la fecha de vencimiento no sea anterior a hoy
        fecha_vencimiento = form.cleaned_data.get('fecha_vencimiento')
        if fecha_vencimiento and fecha_vencimiento < timezone.now().date():
            form.add_error('fecha_vencimiento', 'La fecha de vencimiento no puede ser anterior a hoy')
            return self.form_invalid(form)
        
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class TareaUpdateView(LoginRequiredMixin, UpdateView):
    model = Tarea
    form_class = TareaForm
    success_url = reverse_lazy('tareas:tarea_list')
    template_name = 'tareas/tarea_form.html'

    def get_queryset(self):
        return Tarea.objects.filter(usuario=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        """Bloquea edición de tareas completadas o vencidas"""
        tarea = self.get_object()
        if tarea.completada:
            messages.error(request, 'No se puede editar una tarea completada.')
            return redirect('tareas:tarea_list')
        if tarea.esta_vencida():
            messages.error(request, 'No se puede editar una tarea vencida.')
            return redirect('tareas:tarea_list')
        return super().dispatch(request, *args, **kwargs)

@login_required
@require_POST
def marcar_completada(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk, usuario=request.user)
    
    # No permitir marcar/desmarcar si está vencida
    if tarea.esta_vencida():
        messages.error(request, 'No se puede modificar una tarea vencida.')
        return HttpResponseRedirect(reverse('tareas:tarea_list'))
    
    # Cambiar estado
    tarea.completada = not tarea.completada
    tarea.save()
    
    if tarea.completada:
        messages.success(request, '¡Tarea completada!')
    else:
        messages.success(request, 'Tarea marcada como pendiente.')
    
    return HttpResponseRedirect(reverse('tareas:tarea_list'))

class TareaDeleteView(LoginRequiredMixin, DeleteView):
    model = Tarea
    success_url = reverse_lazy('tareas:tarea_list')
    template_name = 'tareas/tarea_confirm_delete.html'

    def get_queryset(self):
        return Tarea.objects.filter(usuario=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        tarea = self.get_object()
        if tarea.cancelada or tarea.esta_vencida():
            messages.warning(request, '⚠️ La tarea ya estaba cancelada/vencida, puedes eliminarla')
        return super().dispatch(request, *args, **kwargs)

@login_required
@require_POST
def marcar_completada(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk, usuario=request.user)
    
    # No permitir marcar como completada si está vencida o cancelada
    if tarea.cancelada or tarea.esta_vencida():
        messages.error(request, '❌ No puedes modificar una tarea vencida o cancelada')
        return HttpResponseRedirect(reverse('tareas:tarea_list'))
    
    tarea.completada = not tarea.completada
    tarea.save()
    
    estado = "completada" if tarea.completada else "pendiente"
    messages.success(request, f'✅ Tarea marcada como {estado}')
    return HttpResponseRedirect(reverse('tareas:tarea_list'))