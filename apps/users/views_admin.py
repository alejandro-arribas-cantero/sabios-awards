from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, View
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = UserCreationForm()
        return context

class UserCreateView(AdminRequiredMixin, View):
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Usuario {user.username} creado correctamente.")
            return redirect('admin_user_list')
        
        # If invalid, render the list again with errors
        users = User.objects.all().order_by('-date_joined')
        # We can implement simple pagination here if needed, or just show first page
        # For simplicity in this error case, we just show the first 20 or all?
        # Let's just pass the queryset. The template might expect 'page_obj' if we aren't careful.
        # Check template.
        
        # Template uses 'users' loop. 'page_obj' is used for pagination links.
        # If we just pass 'users' (queryset) and no page_obj, the loop works.
        # The pagination controls check 'if is_paginated'.
        # So we just don't pass 'is_paginated=True'.
        
        return render(request, 'users/admin/user_list.html', {
            'users': users[:20], # Show first 20 to avoid huge list
            'form': form,
            'show_modal': True # Flag to reopen modal
        })

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
