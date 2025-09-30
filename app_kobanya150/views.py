from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from django.http import HttpRequest, HttpResponse

from .models import *

from django.contrib import messages

import datetime



# Create your views here.



def index(request: HttpRequest) -> HttpResponse:
    idoszak = kobanya150_Idoszak.objects.all().order_by('-kezdoDatum').first()
    alkalmak = kobanya150_Alkalom.objects.filter(idoszak=idoszak).order_by('datum', 'ido_kezdes') if idoszak else []
    is_in_any = kobanya150_Alkalom.objects.filter(jelentkezok=request.user).exists()
    context = {

        'idoszak': idoszak,
        'alkalmak': alkalmak,
        'is_in_any': is_in_any,

    }
    return render(request, 'kobanya150/index.html', context)

def feljelentkezes(request: HttpRequest, id: int) -> HttpResponse:
    if request.method == 'POST':

        alkalom = kobanya150_Alkalom.objects.get(id=id)
        alkalom.jelentkezes(request.user)
        print(f"Feljelentkezés sikeres: {request.user} az alkalomra {alkalom}")

    return redirect('kobanya150_index')

def lejelentkezes(request: HttpRequest, id: int) -> HttpResponse:
    if request.method == 'POST':

        alkalom = kobanya150_Alkalom.objects.get(id=id)
        alkalom.lejelentkezes(request.user)
        print(f"Lemondás sikeres: {request.user} az alkalomról {alkalom}")

    return redirect('kobanya150_index')

def atjelentkezes(request: HttpRequest, id: int) -> HttpResponse:
    if request.method == 'POST':

        alkalom = kobanya150_Alkalom.objects.get(id=id)
        alkalom.atjelentkezes(request.user)
        print(f"Átjelentkezés sikeres: {request.user} az alkalomról {alkalom}")

    return redirect('kobanya150_index')

