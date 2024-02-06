from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import logout

class LoginRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.path == reverse('base:login'):
                return redirect('base:index', id = request.user.id)
        else:
            allowed_paths = [reverse('base:login'), reverse('base:register', args = ['Driver']), reverse('base:register', args = ['Passenger'])]
            if request.path not in allowed_paths:
                return redirect('base:login')

        response = self.get_response(request)
        return response
