from django.urls import path, register_converter

from women import views, converters

register_converter(converters.FourDigitYearConverter, "yyyy")


urlpatterns = [
    path("", views.index),
    path("cats/", views.categories),
    path("cats/<int:cat_id>/", views.categories_by_id),
    path("archive/<yyyy:year>/", views.archive)
]
