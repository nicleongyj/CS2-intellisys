from django.urls import path
from . import views

urlpatterns = [
    path('liveCam1/', views.LiveCam1, name='liveCam1'),
    path('liveCam2/', views.LiveCam2, name='liveCam2'),
    path('videoList/', views.listpage, name='videoList'),
    path('deleteList/$', views.deleteList, name='deleteList'),
    path('videoFeed1', views.video_feed1, name='videoFeed1'),
    path('videoFeed2', views.video_feed2, name='videoFeed2'),
    path('videoFeed3', views.video_feed3, name='videoFeed3'),
    path('update_details', views.update_detection, name='update_details'),
    path('update_details1', views.update_detection1, name='update_details1'),
    path('garbagechute/', views.garbagechute, name='garbagechute'),
    path('sample/', views.sample, name='sample'),
    path('evidence/', views.evidence, name='evidence'),
    path('', views.index, name='index'),
]
