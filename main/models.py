from django.db import models


# Create your models here.

class Video(models.Model):
    video = models.FileField()

    def _str_(self):
        return self.video.name


