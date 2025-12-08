from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # List of paths that don't require authentication
        exempt_urls = [
            reverse('login'),

            '/admin/', # Django admin has its own auth
        ]
        
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return self.get_response(request)

        if not request.user.is_authenticated:
            # Check if current path is exempt
            is_exempt = False
            for url in exempt_urls:
                if request.path.startswith(url):
                    is_exempt = True
                    break
            
            if not is_exempt:
                return redirect(settings.LOGIN_URL)

        response = self.get_response(request)
        return response
