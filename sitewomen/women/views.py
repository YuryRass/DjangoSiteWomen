from django.http import HttpResponse, HttpRequest


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Главная страница приложения women.')
