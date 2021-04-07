from django.shortcuts import render, HttpResponse, redirect
from quiz.base.models import Pergunta, Aluno, Resposta
from quiz.base.forms import AlunoForm
from django.db.models import Sum
# from django.utils import HttpResponse

# Create your views here.
def home(requisicao):
	if requisicao.method == "POST":
		# se usuario ja existe
		email = requisicao.POST['email']
		try:
			aluno = Aluno.objects.get(email=email)
		except Aluno.DoesNotExist:

			# não existe
			formulario = AlunoForm(requisicao.POST)  # Extrai os dados da requisição
			print('FORM-->', formulario)
			if formulario.is_valid():
				aluno = formulario.save()  # salva os dados no db
				requisicao.session['aluno_nome'] = aluno.nome
				requisicao.session['aluno_id'] = aluno.id  # atribui id do aluno a sessão
				# redireciona para as perguntas
				return redirect('/game/1')
			else:
				contexto = {'formulario': formulario}  # dados da requisição
				return render(requisicao, 'base/index.html', contexto)

		else:
			# sessão do usuário
			requisicao.session['aluno_nome'] = aluno.nome
			requisicao.session['aluno_id'] = aluno.id
			return redirect('/game/1')
	else:
		return render(requisicao, 'base/index.html')

def end(requisicao):
	try:
		# recupera o aluno id da sessão
		aluno_id = requisicao.session['aluno_id']
		aluno_nome = requisicao.session['aluno_nome']

	except KeyError:
		return redirect('/')
	else:
		# aggregate junta e soma em um dict de mesmo nome
		pontos_dct = Resposta.objects.filter(aluno_id=aluno_id).aggregate(Sum('pontos'))
		pontuacao_do_aluno = pontos_dct['pontos__sum']
		# pontos__sum__gt soma dos pontos é maior que
		numero_de_alunos_com_maior_pontuacao = Resposta.objects.values('pontos').annotate(Sum('pontos')).filter(pontos__sum__gt=pontuacao_do_aluno).count()
		# order_by('-pontos__sum') '-' do menor para o maior
		primeiros_alunos_da_classificacao = list(
			Resposta.objects.values('aluno', 'aluno__nome').annotate(Sum('pontos')).order_by('-pontos__sum')[:5]
		)

		contexto = {
			'pontuacao_do_aluno': pontuacao_do_aluno,
			'posicao_do_aluno': numero_de_alunos_com_maior_pontuacao + 1,
			'primeiros_alunos_da_classificacao': primeiros_alunos_da_classificacao,
		}

		return render(requisicao, 'base/end.html', contexto)


from django.utils import timezone
PONTUACAO_MAXIMA = 1000
def game(requisicao, indice):
	try:
		# recupera o aluno id da sessão
		aluno_id = requisicao.session['aluno_id']
		aluno_nome = requisicao.session['aluno_nome']

	except KeyError:
		return redirect('/')
	else:
		try:
			pergunta = Pergunta.objects.filter(disponivel=True).order_by('id')[indice - 1]
		except IndexError:
			return redirect('/end')
		else:
			contexto = {
				'indice_da_questao': indice,
				'pergunta': pergunta,
				'aluno_id': aluno_id,
				'aluno_nome': aluno_nome,
			}
			if requisicao.method == 'POST':
				resposta_indice = int(requisicao.POST['resposta_indice'])
				if resposta_indice == pergunta.alternativa_correta:
					# Armazenar dados da resposta
					try:
						data_da_primeira_resposta = Resposta.objects.filter(pergunta=pergunta).order_by('respondida_em')[0].respondida_em
						print(data_da_primeira_resposta)
					except IndexError:
						Resposta(aluno_id=aluno_id,pergunta=pergunta,pontos=PONTUACAO_MAXIMA).save()
					else:
						print(f'datetime-->{timezone.now()}')
						diferenca = timezone.now() - data_da_primeira_resposta
						diferenca_em_segundos = int(diferenca.total_seconds())
						# se for menor que dez, retorna 10
						pontos = max(PONTUACAO_MAXIMA - diferenca_em_segundos, 10)
						Resposta(aluno_id=aluno_id,pergunta=pergunta,pontos=pontos).save()

					return redirect(f'/game/{indice + 1}')
				else:
					contexto['resposta_indice'] = resposta_indice

			return render(requisicao, 'base/game.html', contexto)
		