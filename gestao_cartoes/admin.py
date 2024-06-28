# admin.py
from django.contrib import admin
from .models import Cartao, Gasto

admin.site.register(Cartao)
admin.site.register(Gasto)