
from bs4 import BeautifulSoup
import requests
import re
import os
import operator
import datetime
from urllib.parse import urljoin
from .models import GpxFile,GpxUrl,GpxJoinFile
from django.conf import settings
from django.core.files import File

class JoinedGpxFile:
    def __init__(self):
        pass

class StravaJoin:
    def __init__(self,request,url_list):
        self.request=request
        self.url_list=url_list
        self.data_list=[]
        self.instance=JoinedGpxFile()

    def run(self):
        self.__add_data_list()
        self.__create_gpxfile_name()
        self.__write()

    def __add_data_list(self):
        for url in self.url_list:
            gpxfile_obj=GpxUrl.objects.filter(user=self.request.user,url=url)[0].gpxfile.all()[0] #urlに紐づかれたfileを取得する
            self.data_list.append({'data':gpxfile_obj,'time':gpxfile_obj.time})

        #metadataのtime順にdata_listを並び替える
        self.data_list=sorted(self.data_list, key=operator.itemgetter('time'))

    def __create_gpxfile_name(self):
        #gpxファイルを結合してできた新しいgpxファイル名を現在の年月日時秒から作成する
        self.instance.filename=re.sub(r'[\s|:|\.|-]','', str(datetime.datetime.now()))+'.gpx'

    def __write(self):
        #gpxファイルの結合を行い、gpxファイルのfileobjectを返す
        with open(self.instance.filename,mode='a+',encoding='utf-8') as fa:
            fa.truncate(0) #ファイルに書かれている物を削除する
            for count,data in enumerate(self.data_list):
                fileurl=str(settings.BASE_DIR)+data['data'].file.url #fileのパスを絶対パスに変換
                print(fileurl)
                if count == 0:
                    with open(fileurl,'r+',encoding='utf-8') as fr:
                        self.write_first(fr,fa)   
                elif 0< count < len(self.data_list)-1:
                    with open(fileurl,'r+',encoding='utf-8') as fr:
                        self.write_trkseg(fr,fa)
                else:
                    with open(fileurl,'r+',encoding='utf-8') as fr:
                        self.write_trkseg(fr,fa)
                        print('</trkseg></trk></gpx>',file=fa)
            
            GpxJoinFile.objects.create(user=self.request.user,file=File(fa))
        
        os.remove(os.path.abspath(self.instance.filename))
    
    def write_first(self,fr,fa):
        trkseg_bool=True
        for line in fr:
            if '<name>' in line:
                line=re.sub(r'<name>.+</name>','<name>ride</name>',line)
            if '</trkseg>' in line:
                trkseg_bool=False
            if trkseg_bool:
                print(line,file=fa)
    
    def write_trkseg(self,fr,fa):
        trkseg_bool=False
        for line in fr:
            if 'trkseg' in line:
                trkseg_bool=not trkseg_bool
            if trkseg_bool and not ('trkseg' in line):
                print(line,file=fa)











