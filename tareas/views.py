from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
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

# Vistas de tareas
class TareaListView(LoginRequiredMixin, ListView):
    model = Tarea
    context_object_name = 'tareas'
    template_name = 'tareas/tarea_list.html'

    def get_queryset(self):
        return Tarea.objects.filter(usuario=self.request.user)

class TareaCreateView(LoginRequiredMixin, CreateView):
    model = Tarea
    form_class = TareaForm
    success_url = reverse_lazy('tareas:tarea_list')
    template_name = 'tareas/tarea_form.html'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class TareaUpdateView(LoginRequiredMixin, UpdateView):
    model = Tarea
    form_class = TareaForm
    success_url = reverse_lazy('tareas:tarea_list')
    template_name = 'tareas/tarea_form.html'

    def get_queryset(self):
        return Tarea.objects.filter(usuario=self.request.user)

class TareaDeleteView(LoginRequiredMixin, DeleteView):
    model = Tarea
    success_url = reverse_lazy('tareas:tarea_list')
    template_name = 'tareas/tarea_confirm_delete.html'

    def get_queryset(self):
        return Tarea.objects.filter(usuario=self.request.user)

# Vista para marcar como completada/pendiente (toggle)
@login_required
@require_POST
def marcar_completada(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk, usuario=request.user)
    tarea.completada = not tarea.completada
    tarea.save()
    return HttpResponseRedirect(reverse('tareas:tarea_list'))