from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
from re import search
import pytz

def tagja(a_user, csoportnev):
    return a_user.groups.filter(name=csoportnev).exists()

# def admin(a_user):
#     return tagja(a_user, 'admin')

# def tanar(a_user):
#     return tagja(a_user, 'tanar')

def dictzip(szoveg):
    sorok = szoveg.strip().split('\n')
    mezonevek = sorok[0].strip().split('\t')+['sor']
    rekordok = list(map(lambda sor : dict(zip(mezonevek, sor.strip().split('\t')+[sor])), sorok[1:]))
    return rekordok

def get_or_error(klassz, az_id):
    a_cucc = klassz.objects.filter(id=az_id).first()
    if a_cucc == None:
        print(f"ezt az id-t kérték le a {klassz} classból, de ilyen nincs: {az_id}, ezért kap egy 404-et")
        return (None, Response(status=status.HTTP_404_NOT_FOUND))
    return (a_cucc, None)

def mezonev_check(s, mezonevek):
    st = s.split('\n')
    t = st[0].split('\t')
    melyikhianyzik = []
    
    for mezonev in mezonevek:
        if mezonev not in t:
            melyikhianyzik.append(mezonev)
    
    return (melyikhianyzik, len(melyikhianyzik)==0)

def get_or_create_user(rekord):
    a_user = User.objects.filter(username=rekord['username']).first()
    if a_user != None:
        return (a_user, False)
    a_user = User.objects.create_user(  username = rekord['username'],
                                        email = rekord['email'],
                                        password = rekord['password'],
                                        last_name = rekord['last_name'],
                                        first_name = rekord['first_name'],
                                        )
    return (a_user, True)


def int_or_None(s):
    try:
        return int(s)
    except:
        return None
    
def helyi_idobe(dt):
    return timezone.localtime(dt, pytz.timezone('Europe/Budapest'))

def szepdatumido(dt:datetime):
    return dt.strftime(r'%Y.%m.%d. %H:%M')


def tanaremail2slug(email:str) -> str:
    nev = search(r'(.*)\.(.*)@szlgbp\.hu', email)
    return f'{nev.group(1)}_{nev.group(2)}'


def egesz(x):
    try:
        return int(x)
    except:
        return None



def tabla_tsv_stringbe(a_model):
    mezok = [o.name for o in a_model._meta.fields]
    print(mezok)
    s = ''
    for mezo in mezok:
        s+=mezo+'\t'
    print(s)
    for sor in a_model.objects.all():        
        for mezo in mezok:
            s+= str(getattr(sor, mezo))+'\t'
        s+='\n'
    return s
