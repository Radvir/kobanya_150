from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from django.http import HttpRequest, HttpResponse

from .models import *

from django.contrib import messages

import datetime



# Create your views here.



def index(request: HttpRequest) -> HttpResponse:
    idoszak = kobanya150_Idoszak.objects.all().order_by('-kezdoDatum').first()
    alkalmak = kobanya150_Alkalom.objects.filter(idoszak=idoszak).order_by('datum') if idoszak else []
    context = {

        'idoszak': idoszak,
        'alkalmak': alkalmak,

    }
    render(request, 'kobanya150/index.html', context)
    

