
from django.shortcuts import redirect

def no_direct_call(func):
    def inner_view(request):
        if request.POST.getlist('activitydata'):
            return func(request)
        else:
            return redirect('stravajoin:index')
    return inner_view
    