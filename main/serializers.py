from rest_framework import serializers
from .models import Objects, Todo


class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objects
        fields = ('objectId', 'name', 'detected')

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('task', 'description')
