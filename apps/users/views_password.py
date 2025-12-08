from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Profile

class ForcePasswordChangeView(PasswordChangeView):
    template_name = 'users/force_password_change.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Update the profile to disable the force flag
        profile = self.request.user.profile
        profile.force_password_change = False
        profile.save()
        messages.success(self.request, "Tu contraseña ha sido actualizada correctamente. ¡Gracias!")
        return response
