from django.contrib.auth.models import User
from django.views import generic
from rest_framework import viewsets

from .models import JeKer
from .serializers import JeKerSerializer, UserSerializer

# Create your views here.
class JeKerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows jeKers to be viewed or edited.
    """
    queryset = JeKer.objects.all().order_by('name')
    serializer_class = JeKerSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer



class IndexView(generic.ListView):
    template_name = 'jeKers/index.html'
    context_object_name = 'all_jeKers'

    def get_queryset(self):
        return JeKer.objects.all()

class B3View(generic.ListView):
    template_name = 'jeKers/b3.html'
    context_object_name = 'present_jeKers'

    def get_queryset(self):
        return JeKer.objects.filter(presence=True).all()
