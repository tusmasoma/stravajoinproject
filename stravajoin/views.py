from django.shortcuts import render
from django.core.files import File
from django.contrib.auth.decorators import login_required
from .strava_scrape import ScrapeMyActivity
from .strava_join import StravaJoin
from .models import GpxFile,GpxUrl,GpxJoinFile,MyActivity
from .decoraters import no_direct_call

@login_required(login_url='accounts:login')
def index_view(request):
    datalist=MyActivity.objects.filter(user=request.user)
    return render(request,'stravajoin/index.html',{'datalist':enumerate(datalist)})

@no_direct_call
def join_view(request):
    sj=StravaJoin(request,request.POST.getlist('activitydata'))
    print(request.POST.getlist('activitydata'))
    sj.run()

    file_obj=GpxJoinFile.objects.filter(user=request.user).latest('id')
    mb=f'{int(file_obj.file.size)/1024/1024:.2f}'

    return render(request,'stravajoin/result.html',{'file_obj':file_obj})