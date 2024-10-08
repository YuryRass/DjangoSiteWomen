from typing import Any
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.urls.exceptions import Resolver404
from django.views import View
from django.views.generic import TemplateView, ListView, DeleteView
from women.forms import AddPostForm, UploadFilesForm
from women.models import Category, TagPost, Women, UploadFiles

# from django.template.loader import render_to_string


menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    {"title": "Войти", "url_name": "login"},
]


# def index(request: HttpRequest) -> HttpResponse:
#     posts = Women.published.all().select_related("cat")
#     data = {
#         "title": "Главная страница",
#         "menu": menu,
#         "posts": posts,
#         "cat_selected": 0,
#     }
#     return render(request, "women/index.html", data)


class HomeWomen(ListView):
    template_name = "women/index.html"
    context_object_name = "posts"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Главная страница"
        context["menu"] = menu
        context["cat_selected"] = 0
        return context

    def get_queryset(self) -> QuerySet[Any]:
        return Women.published.all().select_related("cat")


def write_file(uploaded_file: InMemoryUploadedFile):
    with open(f"sitewomen/uploads/{uploaded_file.name}", "wb") as upl_file:
        for chunk in uploaded_file.chunks():
            upl_file.write(chunk)


def about(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UploadFilesForm(request.POST, request.FILES)
        if form.is_valid():
            # write_file(form.cleaned_data['file'])
            new_file = UploadFiles(file=form.cleaned_data["file"])
            new_file.save()
    else:
        form = UploadFilesForm()

    return render(
        request,
        "women/about.html",
        {"menu": menu, "title": "Сайт о женщинах", "form": form},
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


class ShowPost(DeleteView):
    model = Women
    context_object_name = 'post'
    template_name = "women/post.html"
    slug_url_kwarg = "post_slug"  # pk_url_kwarg - для ID

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title
        context['menu'] = menu
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])



class AddPage(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = AddPostForm()
        return render(
            request,
            "women/addpage.html",
            {
                "menu": menu,
                "title": "Добавление статьи",
                "form": form,
            },
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")


def contact(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Обратная связь")


def login(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Авторизация")


class WomenCategory(ListView):
    template_name = "women/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context["posts"][0].cat
        context["title"] = "Категория - " + cat.name
        context["menu"] = menu
        context["cat_selected"] = cat.id
        return context

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs["cat_slug"]).select_related(
            "cat"
        )


def page_not_found(
    request: HttpRequest, exception: Resolver404
) -> HttpResponseNotFound:
    return HttpResponseNotFound("<h1>Страница не найдена!</h1>")


# def show_tag_postlist(request: HttpRequest, tag_slug: str) -> HttpResponse:
#     tag: TagPost = get_object_or_404(TagPost, slug=tag_slug)
#     posts = tag.women.filter(is_published=Women.Status.PUBLISHED).select_related("cat")
#     data = {
#         "title": f"Тег: {tag.tag}",
#         "menu": menu,
#         "posts": posts,
#         "cat_selected": None,
#     }

#     return render(request, "women/index.html", context=data)


class ShowTagPostList(ListView):
    template_name = "women/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(
            tags__slug=self.kwargs["tag_slug"]
        ).select_related("cat")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs["tag_slug"])
        context["title"] = "Тег - " + tag.tag
        context["menu"] = menu
        context["cat_selected"] = None
        return context
