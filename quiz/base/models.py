from django.db import models

# Create your models here.
class Pergunta(models.Model):
	ALTERNATIVAS = [
		(0, 'A'),
		(1, 'B'),
		(2, 'C'),
		(3, 'D'),
	]
	enunciado = models.TextField()
	disponivel = models.BooleanField(default = False)
	alternativas = models.JSONField()
	alternativa_correta = models.IntegerField(ALTERNATIVAS)