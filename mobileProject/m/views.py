from django.shortcuts import render
from m.indexapi import index as indexApi
from django.http import HttpResponse
import json
# Create your views here.

def index(request):
    '''收页'''
    data = indexApi.api.index(request)
    if data is False:
        return render(request,'index.html')
    print({'data':data})
    return render(request, 'index.html', {'data':data})


def page(request):
    '''分页'''
    data = indexApi.api.index(request)
    if data is not False:
        return render(request, 'page.html', {'data':data})
    return None