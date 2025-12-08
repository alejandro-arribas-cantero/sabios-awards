from django.shortcuts import redirect
from django.urls import reverse

class ForcePasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_superuser:
            try:
                profile = request.user.profile
                if profile.force_password_change:
                    # Allowed paths
                    password_change_url = reverse('password_change')
                    logout_url = reverse('logout')
                    
                    if request.path not in [password_change_url, logout_url]:
                        return redirect('password_change')
            except:
                pass
        
        response = self.get_response(request)
        return response
