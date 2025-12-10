from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            path = request.path
            try:
                login_url = reverse('login')
            except:
                login_url = '/auth/login/' # Fallback
            
            # Allow access to login page
            if path == login_url:
                return self.get_response(request)
                
            # Allow access to static and media files
            if path.startswith(settings.STATIC_URL) or path.startswith(settings.MEDIA_URL):
                return self.get_response(request)
            
            # Redirect to login
            return redirect(f"{login_url}?next={path}")
            
        return self.get_response(request)

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

