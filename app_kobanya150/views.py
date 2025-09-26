from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from django.http import HttpRequest, HttpResponse

from .models import *

from django.contrib import messages

import datetime



# Create your views here.



def index(request: HttpRequest) -> HttpResponse:

    # """

    # Main view showing current school year and available weeks

    # """

    # # Ensure current school year exists

    # current_tanev = tanev_fix()

    

    # # Get upcoming weeks (from today onwards)

    # today = datetime.date.today()

    # upcoming_weeks = Het.objects.filter(

    #     tanev=current_tanev,

    #     hetfoDatum__gte=today

    # ).order_by('hetfoDatum')[:10]  # Show next 10 weeks

    

    # # Get current week if exists

    # current_week = Het.objects.filter(

    #     tanev=current_tanev,

    #     hetfoDatum__lte=today,

    #     hetfoDatum__gt=today - datetime.timedelta(days=7)

    # ).first()

    

    # context = {

    #     'title': 'RePont - Heti Jelentkezés',

    #     'current_tanev': current_tanev,

    #     'upcoming_weeks': upcoming_weeks,

    #     'current_week': current_week,

    #     'today': today

    # }

    return render(request, 'repont/index.html') #, context)



@login_required

def jelentkezes(request: HttpRequest, het_id: int):

    """

    View for students to sign up for a specific week

    """

    try:

        het = Het.objects.get(id=het_id)

    except Het.DoesNotExist:

        messages.error(request, 'A kért hét nem található.')

        return redirect('repont_index')

    

    # Check if week is in the future

    if het.hetfoDatum < datetime.date.today():

        messages.error(request, 'Csak jövőbeli hetekre lehet jelentkezni.')

        return redirect('repont_index')

    

    # Check if user is already signed up

    if request.user in het.diakok.all():

        messages.warning(request, 'Már jelentkeztél erre a hétre.')

        return redirect('repont_index')

    

    # Check if there's space

    if not het.lehet_jelentkezni():

        messages.error(request, 'Erre a hétre már nincs szabad hely (max 2 diák).')

        return redirect('repont_index')

    

    # Sign up the user

    het.diakok.add(request.user)

    messages.success(request, f'Sikeresen jelentkeztél a(z) {het.hetfoDatum} hetére.')

    

    return redirect('repont_index')



@login_required

def leiratkozas(request: HttpRequest, het_id: int):

    """

    View for students to unsubscribe from a specific week

    """

    try:

        het = Het.objects.get(id=het_id)

    except Het.DoesNotExist:

        messages.error(request, 'A kért hét nem található.')

        return redirect('repont_index')

    

    # Check if week is in the future

    if het.hetfoDatum < datetime.date.today():

        messages.error(request, 'Múltbeli hetekről nem lehet leiratkozni.')

        return redirect('repont_index')

    

    # Check if user is signed up

    if request.user not in het.diakok.all():

        messages.warning(request, 'Nem vagy jelentkezve erre a hétre.')

        return redirect('repont_index')

    

    # Remove the user

    het.diakok.remove(request.user)

    messages.success(request, f'Sikeresen leiratkoztál a(z) {het.hetfoDatum} hetéről.')

    

    return redirect('repont_index')



def error_response(request: HttpRequest, message: str = "Page not found", status: int = 404):

    """

    Generic error response view

    """

    return render(request, 'repont/error.html', {

        'message': message, 

        'status': status

    }, status=status)