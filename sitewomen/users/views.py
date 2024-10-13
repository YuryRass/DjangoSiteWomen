from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from django.views.generic import CreateView, UpdateView

from django.urls import reverse_lazy
from typing import Any
from users.forms import LoginUserForm, ProfileUserForm, RegisterUserForm


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': "Авторизация"}

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('users:login')

class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': "Профиль пользователя"}

    def get_success_url(self) -> Any:
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None) -> AbstractBaseUser | AnonymousUser:
        return self.request.user