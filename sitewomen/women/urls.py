from django.urls import path, register_converter

from women import views, converters

register_converter(converters.FourDigitYearConverter, "yyyy")


urlpatterns = [
    path("", views.index, name='home'),
    path("about/", views.about, name="about"),
    path("cats/", views.categories, name='cats'),
    path("cats/<int:cat_id>/", views.categories_by_id, name='cats_by_id'),
    path("archive/<yyyy:year>/", views.archive, name='archive'),
    path("post/<int:post_id>", views.show_post, name="post"),
    path("about/", views.about, name="about"),
    path("add/", views.add, name="add_page"),
    path("contact/", views.contact, name="contact"),
    path("login/", views.login, name="login")
]
