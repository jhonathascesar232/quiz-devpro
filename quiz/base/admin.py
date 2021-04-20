from django.contrib import admin

from .models import Aluno, Pergunta, Resposta


# Register your models here.
@admin.register(Pergunta)
class PergundaAdmin(admin.ModelAdmin):
	list_display = ('id', 'enunciado', 'disponivel')

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
	list_display = ('nome', 'email', 'criado_em')

@admin.register(Resposta)
class RespostaAdmin(admin.ModelAdmin):
	list_display = ('respondida_em', 'aluno', 'pergunta', 'pontos')
