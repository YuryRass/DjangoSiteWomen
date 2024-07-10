from django.http import HttpResponse, HttpRequest, HttpResponseNotFound
from django.shortcuts import redirect, reverse, render
# from django.template.loader import render_to_string

from django.urls.exceptions import Resolver404

data_db = [
    {'id': 1, 'title': 'Анджелина Джоли', 'content': 'Биография Анджелины Джоли', 'is_published': True},
    {'id': 2, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'is_published': False},
    {'id': 3, 'title': 'Джулия Робертс', 'content': 'Биография Джулия Робертс', 'is_published': True},
]

menu = ["О сайте", "Добавить статью", "Обратная связь", "Войти"]


def index(request: HttpRequest) -> HttpResponse:
    # t = render_to_string('women/index.html')
    # return HttpResponse(t)
    context = {
        'menu': menu,
        'title': 'Главная страница',
        'posts': data_db,
    }
    return render(request, 'women/index.html', context)


def about(request: HttpRequest) -> HttpResponse:
    return render(request, "women/about.html")


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
