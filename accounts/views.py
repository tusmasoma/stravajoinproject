
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
import re
from .strava_accounts import login_strava_by_requests
from .strava_scrape import ScrapeMyActivity
from .strava_filesave import SaveGpxFile
from .decoraters import is_logined
from stravajoin.models import MyActivity


@is_logined
def login_view(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']
        username=re.search(r'(.+)@.+',email).group(1)

        user_obj=authenticate(request,username=username,email=email,password=password)

        if user_obj is not None:
            login(request,user_obj)

            sma=ScrapeMyActivity.get_instance(email,password)
            sma.run()

            session=login_strava_by_requests(email,password)

            MyActivity.objects.filter(user=request.user).delete()

            for data in sma.datalist:
                sgf=SaveGpxFile(request,session[0],data)
                sgf.run()
                MyActivity.objects.create(user=request.user,**data.__dict__)

            return redirect('stravajoin:index')

        else:
            return render(request,'accounts/login.html',{'loginDenied':True})
    else:
        return render(request,'accounts/login.html')



def logout_view(request):
    logout(request)
    return redirect("stravajoin:index")


@is_logined
def signup_view(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']
        username=re.search(r'(.+)@.+',email).group(1)

        user_obj=authenticate(request,username=username,email=email,password=password)

        if not user_obj:
            registration=login_strava_by_requests(email,password)
            if registration[1]:
                User.objects.create_user(username,email,password)
                return redirect('accounts:login')
            else:
                return render(request,'accounts/signup.html',{'notRegistered':True})
        else:
            return render(request,'accounts/signup.html',{'alreadyRegistered':True})
    else:
        return render(request,'accounts/signup.html')

