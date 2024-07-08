from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, Http404
from django.shortcuts import redirect, reverse
from django.urls.exceptions import Resolver404


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Главная страница приложения women.')


def categories(request: HttpRequest) -> HttpResponse:
    return HttpResponse("<h1>Категории статей</h1>")


def categories_by_id(request: HttpRequest, cat_id: int) -> HttpResponse:
    return HttpResponse(f"<h1>Категория по ID</h1><p>ID: {cat_id}</p>")


def archive(request: HttpRequest, year: int) -> HttpResponse:
    if year > 2024:
        redirect_url = reverse('home')
        return redirect(redirect_url, permanent=True)  # 301
    return HttpResponse(f"<h1>Архив по годам</h1><p>Year: {year}</p>")


def page_not_found(request: HttpRequest, exception: Resolver404) -> HttpResponseNotFound:
    return HttpResponseNotFound("<h1>Страница не найдена!</h1>")
