from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.urls.exceptions import Resolver404
from women.models import Category, TagPost, Women

# from django.template.loader import render_to_string


menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    {"title": "Войти", "url_name": "login"},
]


def index(request: HttpRequest) -> HttpResponse:
    posts = Women.published.all().select_related("cat")
    data = {
        "title": "Главная страница",
        "menu": menu,
        "posts": posts,
        "cat_selected": 0,
    }
    return render(request, "women/index.html", data)


def about(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "women/about.html",
        {"menu": menu, "title": "Сайт о женщинах"},
    )


def categories(request: HttpRequest) -> HttpResponse:
    return HttpResponse("<h1>Категории статей</h1>")


def categories_by_id(request: HttpRequest, cat_id: int) -> HttpResponse:
    return HttpResponse(f"<h1>Категория по ID</h1><p>ID: {cat_id}</p>")


def archive(request: HttpRequest, year: int) -> HttpResponse:
    if year > 2024:
        redirect_url = reverse("home")
        return redirect(redirect_url, permanent=True)  # 301
    return HttpResponse(f"<h1>Архив по годам</h1><p>Year: {year}</p>")


def show_post(request: HttpRequest, post_slug: str) -> HttpResponse:
    post = get_object_or_404(Women, slug=post_slug)

    data = {
        "title": post.title,
        "menu": menu,
        "post": post,
        "cat_selected": 1,
    }

    return render(request, "women/post.html", context=data)


def addpage(request: HttpRequest) -> HttpResponse:
    return render(request, 'women/addpage.html', {'menu': menu, 'title': 'Добавление статьи'})


def contact(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Обратная связь")


def login(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Авторизация")


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Women.published.filter(cat_id=category.pk).select_related("cat")
    data = {
        "title": f"Рубрика: {category.name}",
        "menu": menu,
        "posts": posts,
        "cat_selected": category.pk,
    }

    return render(request, "women/index.html", context=data)


def page_not_found(
    request: HttpRequest, exception: Resolver404
) -> HttpResponseNotFound:
    return HttpResponseNotFound("<h1>Страница не найдена!</h1>")


def show_tag_postlist(request: HttpRequest, tag_slug: str) -> HttpResponse:
    tag: TagPost = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.women.filter(is_published=Women.Status.PUBLISHED).select_related("cat")
    data = {
        "title": f"Тег: {tag.tag}",
        "menu": menu,
        "posts": posts,
        "cat_selected": None,
    }

    return render(request, "women/index.html", context=data)
