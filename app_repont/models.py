from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

# RePont App models:
# Tanév: kezdoEv, Hét: hetfoDatum ManyToMany diakok int bevetel

# Utils

def tanev_fix():
    # Csekkolja, hogy létezik-e a jelenlegi tanév, ha nem, létrehozza
    # Csekkolja, hogy a tanév hetei léteznek-e, ha nem, létrehozza őket (szeptember 1-től kezdve, minden hétfő egészen június 15-ig)
    ma = datetime.date.today()
    if ma.month >= 9:
        kezdoEv = ma.year
    else:
        kezdoEv = ma.year - 1
    tanev, created = Tanev.objects.get_or_create(kezdoEv=kezdoEv)
    if created:
        # Létre kell hozni a hetek modelljeit is
        szeptember1 = datetime.date(kezdoEv, 9, 1)
        junius15 = datetime.date(kezdoEv + 1, 6, 15)
        # Az első hétfő
        elsoHetfo = szeptember1 + datetime.timedelta(days=(7 - szeptember1.weekday()) % 7)
        hetfoDatum = elsoHetfo
        while hetfoDatum <= junius15:
            Het.objects.create(hetfoDatum=hetfoDatum, tanev=tanev)
            hetfoDatum += datetime.timedelta(days=7)
    return tanev


# Models

class Tanev(models.Model):
    # Tanév kezdő év
    # pl. 2025 a 2025/2026 tanév
    kezdoEv = models.IntegerField()

    def __str__(self):
        return f"Tanév {self.kezdoEv}/{self.kezdoEv + 1}"

class Het(models.Model): 
    # Hétfő dátum
    hetfoDatum = models.DateField()
    tanev = models.ForeignKey(Tanev, on_delete=models.CASCADE, related_name='hetek')
    diakok = models.ManyToManyField(User, blank=True, related_name='hetek')
    bevetel = models.IntegerField(default=0)  # Bevételek összege forintban, majd Django adminban kitölti a HATOK

    def lehet_jelentkezni(self) -> bool:
        # Visszaadja, hogy lehet-e még jelentkezni a hétre (max 2 diák)
        return self.diakok.count() < 2

    def __str__(self):
        return f"Hét {self.hetfoDatum} ({self.tanev})"