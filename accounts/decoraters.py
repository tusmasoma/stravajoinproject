
from django.shortcuts import redirect

def is_logined(func):
    def inner(request):
        if request.user.is_authenticated:
            return redirect('stravajoin:index')
        else:
            return func(request)
    return inner