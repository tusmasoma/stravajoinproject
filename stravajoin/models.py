from django.db import models
from django.contrib.auth.models import User


class GpxUrl(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    url=models.URLField(max_length=250)

    def __str__(self) -> str:
        return self.url
 
class GpxFile(models.Model):
    url=models.ForeignKey(GpxUrl,on_delete=models.CASCADE,related_name='gpxfile')
    file=models.FileField(upload_to='documents/%Y/%m/%d')
    time=models.CharField(max_length=120)

    def __str__(self) -> str:
        return self.file.url


class GpxJoinFile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    file=models.FileField(upload_to='documents/%Y/%m/%d')


class MyActivity(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    activity_type=models.CharField(max_length=120)
    date=models.CharField(max_length=120)
    title=models.CharField(max_length=120)
    time=models.CharField(max_length=120)
    dist=models.CharField(max_length=120)
    elev=models.CharField(max_length=120)
    gpx_url=models.CharField(max_length=120)
    size=models.CharField(max_length=120)

    def __str__(self) -> str:
        return self.date



