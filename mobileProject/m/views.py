from django.shortcuts import render
from m.indexapi import index as indexApi
import time
# Create your views here.

def index(request):
    return render(request,'index.html')