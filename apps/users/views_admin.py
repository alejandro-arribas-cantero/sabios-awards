from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, View
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy

class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class UserListView(AdminRequiredMixin, ListView):
    model = User
    template_name = 'users/admin/user_list.html'
    context_object_name = 'users'
    paginate_by = 20

    def get_queryset(self):
        return User.objects.all().order_by('-date_joined')

class UserToggleActiveView(AdminRequiredMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if user.is_superuser:
            messages.error(request, "No puedes desactivar a un superusuario.")
        else:
            user.is_active = not user.is_active
            user.save()
            status = "activado" if user.is_active else "desactivado"
            messages.success(request, f"Usuario {user.username} {status}.")
        return redirect('admin_user_list')

class UserDeleteView(AdminRequiredMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if user.is_superuser:
            messages.error(request, "No puedes eliminar a un superusuario.")
        else:
            user.delete()
            messages.success(request, f"Usuario {user.username} eliminado.")
        return redirect('admin_user_list')
