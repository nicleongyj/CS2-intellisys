from django.contrib import admin
from .models import *

# Register your models here.

# Model for garbage dumping videos
admin.site.register(Video)

# Model for garbage chute videos
admin.site.register(ChuteVideo)
