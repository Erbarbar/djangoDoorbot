from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse

from .models import JeKer

# Create your views here.

def Index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

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
