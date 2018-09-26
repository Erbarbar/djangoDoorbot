from django.contrib.auth.models import User
from rest_framework import serializers
from .models import JeKer

# Serializers define the API representation.
class JeKerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = JeKer
        fields = ('id' , 'name', 'department', 'status', 'mac_address', 'presence')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email')
