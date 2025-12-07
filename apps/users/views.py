from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import FormView, View
from django.urls import reverse_lazy
from django.contrib import messages

class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Registro exitoso. ¡Bienvenido!")
        return super().form_valid(form)

class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        login(self.request, form.get_user())
        messages.success(self.request, "Has iniciado sesión correctamente.")
        return super().form_valid(form)

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, "Has cerrado sesión.")
        return redirect('login')
