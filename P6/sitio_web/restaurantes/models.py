from django.db import models

# Create your models here.

from pymongo import MongoClient

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

client = MongoClient()
db = client.test                  # base de datos
restaurantes = db.restaurants     # colección

def validar_precio(value):
    if(value < 0):
        raise ValidationError(
            _('El precio debe ser mayor a 0')
        )
    elif(value > 500):
        raise ValidationError(
            _('El precio debe ser mayor a 0')
        )
        

class Platos(models.Model):
    name = models.CharField(max_length=100)
    tipo = models.CharField(max_length=150)
    alergenos = models.TextField()
    #Text field no tiene max_length
    precio = models.FloatField(validators=[validar_precio])
    objects = models.Manager()
    def __str__(self):
        return self.name

    def getTipo(self):
        return self.tipo

    def getAler(self):
        return self.alergenos
    
    def getPrecio(self):
        return self.precio
    
    def getNombre(self):
        return self.name
