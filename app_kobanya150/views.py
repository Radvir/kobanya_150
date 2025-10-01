from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required, user_passes_test

from django.http import HttpRequest, HttpResponse

from .models import *

from django.contrib import messages

import datetime

from datetime import date

# Create your views here.

def jogosult_e(user):
    return user.groups.filter(name='Kobanya150_kezelo').exists()

@login_required(login_url='login')
def index(request: HttpRequest) -> HttpResponse:
    idoszak = kobanya150_Idoszak.objects.all().order_by('-kezdoDatum').first()
    alkalmak = kobanya150_Alkalom.objects.filter(idoszak=idoszak).order_by('datum', 'ido_kezdes') if idoszak else []
    is_in_any = kobanya150_Alkalom.objects.filter(jelentkezok=request.user).exists()
    jogosultsag = jogosult_e(request.user)
    mai_datum = date.today()
    context = {

        'idoszak': idoszak,
        'alkalmak': alkalmak,
        'is_in_any': is_in_any,
        'jogosult_e': jogosultsag,
        'mai_datum': mai_datum,

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



@user_passes_test(jogosult_e)
@login_required
def tablazat(request: HttpRequest) -> HttpResponse:
    idoszakok = kobanya150_Idoszak.objects.all()
    context = {
        'idoszakok': idoszakok,
    }
    return render (request, 'kobanya150/tablazat.html', context)

@user_passes_test(jogosult_e)
@login_required
def tablazat_idoszak(request: HttpRequest, idoszak_id: int) -> HttpResponse:
    idoszak = kobanya150_Idoszak.objects.get(id=idoszak_id)
    alkalmak = kobanya150_Alkalom.objects.filter(idoszak=idoszak).order_by('datum') if idoszak else []
    context = {
        'idoszak': idoszak,
        'alkalmak': alkalmak,
    }
    return render (request, 'kobanya150/tablazat_idoszak.html', context)

@user_passes_test(jogosult_e)
@login_required
def tablazat_alkalom(request: HttpRequest, idoszak_id: int, alkalom_id:int) -> HttpResponse:
    idoszak = kobanya150_Idoszak.objects.get(id=idoszak_id)
    alkalom = kobanya150_Alkalom.objects.get(id=alkalom_id)
    context = {
        'idoszak': idoszak,
        'alkalom': alkalom,
    }
    return render (request, 'kobanya150/tablazat_alkalom.html', context)