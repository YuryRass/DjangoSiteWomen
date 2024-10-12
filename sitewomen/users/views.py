from django.contrib.auth.views import LoginView

from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from users.forms import LoginUserForm
from django.contrib.auth import authenticate, login, logout


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': "Авторизация"}


# def logout_user(request: HttpRequest) -> HttpResponseRedirect:
#     logout(request)
#     return HttpResponseRedirect(reverse('users:login'))