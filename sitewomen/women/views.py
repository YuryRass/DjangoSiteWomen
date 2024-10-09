from typing import Any
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.urls import reverse_lazy
from django.urls.exceptions import Resolver404
from django.views import View
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    DeleteView,
    FormView,
    CreateView,
    UpdateView,
)
from women.mixins import DataMixin
from women.forms import AddPostForm, UploadFilesForm
from women.models import Category, TagPost, Women, UploadFiles

# from django.template.loader import render_to_string


menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    {"title": "Войти", "url_name": "login"},
]


class HomeWomen(DataMixin, ListView):
    template_name = "women/index.html"
    context_object_name = "posts"

    def get_context_data(self, *, object_list=None, **kwargs):
        return self.get_mixin_context(
            super().get_context_data(**kwargs),
            title="Главная страница",
            cat_selected=0,
        )

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


class ShowPost(DataMixin, DetailView):
    context_object_name = "post"
    template_name = "women/post.html"
    slug_url_kwarg = "post_slug"  # pk_url_kwarg - для ID

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context["post"].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(DataMixin, CreateView):
    form_class = AddPostForm
    template_name = "women/addpage.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        return self.get_mixin_context(
            super().get_context_data(**kwargs),
            title="Добавление статьи",
        )


class UpdatePage(DataMixin, UpdateView):
    model = Women
    fields = ["title", "content", "photo", "is_published", "cat"]
    template_name = "women/addpage.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        return self.get_mixin_context(
            super().get_context_data(**kwargs),
            title="Редактирование статьи",
        )


class DeletePage(DataMixin, DeleteView):
    model = Women
    template_name = "women/del_page.html"
    context_object_name = "page"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        return self.get_mixin_context(
            super().get_context_data(**kwargs),
            title="Удаление поста",
        )


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
