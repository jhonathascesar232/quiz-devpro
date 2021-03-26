from django.shortcuts import render, HttpResponse
# from django.utils import HttpResponse

# Create your views here.
def home(requisicao):
	return HttpResponse('Olá Mundo!')