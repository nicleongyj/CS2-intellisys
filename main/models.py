from django.db import models


# Create your models here.

class Video(models.Model):
    video = models.FileField()

    def _str_(self):
        return self.video.name
    
# Model for garbage chute
class ChuteVideo(models.Model):
    video = models.FileField()

    def _str_(self):
        return self.video.name


