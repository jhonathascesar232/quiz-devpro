from django.shortcuts import render, HttpResponse
from quiz.base.models import Pergunta
# from django.utils import HttpResponse

# Create your views here.
def home(requisicao):
	return render(requisicao, 'base/index.html')

def end(requisicao):
	return render(requisicao, 'base/end.html')

def game(requisicao, indice):
	pergunta = Pergunta.objects.filter(disponivel=True).order_by('id')[indice - 1]
	contexto = {'indice_da_questao': indice, 'pergunta': pergunta}
	return render(requisicao, 'base/game.html', context = contexto)
	