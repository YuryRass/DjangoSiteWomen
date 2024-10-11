from django.http import HttpResponse, HttpRequest


def login_user(request: HttpRequest) -> HttpResponse:
    return HttpResponse("login")


def logout_user(request) -> HttpResponse:
    return HttpResponse("logout")
