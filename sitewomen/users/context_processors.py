from women.mixins import menu


def get_women_context(request):
    return {'mainmenu': menu}