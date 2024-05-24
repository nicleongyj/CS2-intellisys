from django.forms import ModelForm
from .models import Video


class DownloadVideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ('video',)
