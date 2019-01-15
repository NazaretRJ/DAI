from django.db import models

# Create your models here.

from pymongo import MongoClient

client = MongoClient()
db = client.test                  # base de datos
restaurantes = db.restaurants     # colección
