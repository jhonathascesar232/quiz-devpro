from django.contrib import admin
from .models import Pergunta


# Register your models here.
@admin.register(Pergunta)
class PergundaAdmin(admin.ModelAdmin):
	list_display = ('id', 'enunciado', 'disponivel')