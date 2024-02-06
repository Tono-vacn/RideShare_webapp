from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import logout

class LoginRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 获取当前用户的登录状态
        if request.user.is_authenticated:
            # 用户已登录，尝试访问登录页面时重定向到index页面
            if request.path == reverse('base:login'):
                return redirect('base:index', id = request.user.id)
        else:
            # 用户未登录，不在登录页面时重定向到登录页面
            if request.path != reverse('base:login'):
                return redirect('base:login')

        response = self.get_response(request)
        return response
