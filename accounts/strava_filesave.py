
from bs4 import BeautifulSoup
import requests
import re
import os
import operator
import datetime
from urllib.parse import urljoin
from django.core.files import File

from stravajoin.models import GpxUrl,GpxFile

class SaveGpxFile:
    """
    一つのgpxfileを保存する
    """
    def __init__(self,request,session,data):
        self.request=request
        self.session=session
        self.data=data

    def run(self):
        self.__save()
        self.__add_size_to_data()

    def __save(self):
        if GpxUrl.objects.filter(user=self.request.user,url=self.data.gpx_url).first() is None:
            gpxurl_obj=GpxUrl(user=self.request.user,url=self.data.gpx_url)
            filename=re.search(r'https://www.strava.com/activities/([0-9]+)/export_gpx',self.data.gpx_url).group(1)+'.gpx'

            with open(filename,"w+", encoding="utf-8") as f:
                    
                gpxfile=self.session.get(self.data.gpx_url)
                f.write(gpxfile.text)

                timedata=re.search(r'<metadata>\s*<time>(.*)</time>\s*</metadata>',gpxfile.text).group(1)
                gpxurl_obj.save() #gpxurlだけ保存され、gpxfileが保存されない場合があるので、保存のタイミングを同じにする
                GpxFile.objects.create(url=gpxurl_obj,file=File(f),time=timedata)
                    
            os.remove(os.path.abspath(filename)) #gpxファイルがサーバー上には保存されないようにします

    def __add_size_to_data(self):
        gpxfile_obj=GpxUrl.objects.filter(user=self.request.user,url=self.data.gpx_url)[0].gpxfile.first()
        size=f'{int(gpxfile_obj.file.size)/1024/1024:.2f}'
        self.data.size=size


    
