from django.shortcuts import render, HttpResponse
# from django.utils import HttpResponse

# Create your views here.
def home(requisicao):
	return render(requisicao, 'base/index.html')

def end(requisicao):
	return render(requisicao, 'base/end.html')

def game(requisicao, indice):
	contexto = {'indice_da_questao': indice}
	return render(requisicao, 'base/game.html', context = contexto)
	