from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

# # Models

class kobanya150_Idoszak(models.Model):  # Időszak neve, pl. "Kőbánya 150 - 2023"
    id = models.AutoField(primary_key=True)
    kezdoDatum = models.DateField()          # Kezdő dátum
    vegDatum = models.DateField()            # Végdátum

    def __str__(self):
        return f"({self.kezdoDatum} - {self.vegDatum})"
    
    class Meta:
        ordering = ['-kezdoDatum']
        verbose_name = "Időszak"
        verbose_name_plural = "Időszakok"


class kobanya150_Alkalom(models.Model):
    id = models.AutoField(primary_key=True)
    datum = models.DateField()
    ido_kezdes = models.TimeField(default=datetime.time(0, 0))
    ido_vege = models.TimeField(default=datetime.time(0, 0))
    idoszak = models.ForeignKey(kobanya150_Idoszak, on_delete=models.CASCADE, related_name='alkalmak')
    jelentkezok = models.ManyToManyField(User, blank=True, related_name='kobanya150_alkalmak')
    max_letszam = models.IntegerField(default=-1)

    def __str__(self):
        return f"{self.idoszak} ({self.datum}: {self.ido_kezdes} - {self.ido_vege}) [{self.jelentkezok.count()}/{self.max_letszam}]"
    
    class Meta:
        ordering = ['-datum']
        verbose_name = "Alkalom"
        verbose_name_plural = "Alkalmak"

    
    def jelentkezes(self, felhasznalo: User):
        if not self.jelentkezok.filter(id=felhasznalo.id).exists() and (self.jelentkezok.count() < self.max_letszam):
            self.jelentkezok.add(felhasznalo)
            return True
        return False
    
    def lejelentkezes(self, felhasznalo: User):
        if self.jelentkezok.filter(id=felhasznalo.id).exists():
            self.jelentkezok.remove(felhasznalo)
            return True
        return False
    
    def atjelentkezes(self, felhasznalo: User):
        for alkalom in kobanya150_Alkalom.objects.filter(idoszak=self.idoszak):
            if alkalom.jelentkezok.filter(id=felhasznalo.id).exists() and (self.jelentkezok.count() < self.max_letszam):
                alkalom.jelentkezok.remove(felhasznalo)
        if not self.jelentkezok.filter(id=felhasznalo.id).exists() and (self.jelentkezok.count() < self.max_letszam):
            self.jelentkezok.add(felhasznalo)
            return True
        return False