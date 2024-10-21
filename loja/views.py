from django.http import JsonResponse
from django.shortcuts import render
from .models import Lanchonete
from datetime import datetime

# View para obter o horário da lanchonete em formato JSON
def exibir_lanchonete(request):
    # Pega a instância única da lanchonete
    lanchonete = Lanchonete.objects.first()

    # Pega o dia da semana atual (0 = segunda, 6 = domingo)
    dia_semana = datetime.today().weekday()

    # Define os horários de acordo com o dia da semana
    horario_inicio = None
    horario_fim = None

    if dia_semana == 0:  # Segunda-feira
        horario_inicio = lanchonete.horario_segunda_inicio
        horario_fim = lanchonete.horario_segunda_fim
    elif dia_semana == 1:  # Terça-feira
        horario_inicio = lanchonete.horario_terca_inicio
        horario_fim = lanchonete.horario_terca_fim
    elif dia_semana == 2:  # Quarta-feira
        horario_inicio = lanchonete.horario_quarta_inicio
        horario_fim = lanchonete.horario_quarta_fim
    elif dia_semana == 3:  # Quinta-feira
        horario_inicio = lanchonete.horario_quinta_inicio
        horario_fim = lanchonete.horario_quinta_fim
    elif dia_semana == 4:  # Sexta-feira
        horario_inicio = lanchonete.horario_sexta_inicio
        horario_fim = lanchonete.horario_sexta_fim
    elif dia_semana == 5:  # Sábado
        horario_inicio = lanchonete.horario_sabado_inicio
        horario_fim = lanchonete.horario_sabado_fim
    elif dia_semana == 6:  # Domingo
        horario_inicio = lanchonete.horario_domingo_inicio
        horario_fim = lanchonete.horario_domingo_fim


  # Retorna os dados em formato JSON
    data = {
        'nome': lanchonete.nome,
        'endereco': lanchonete.endereco,
        'horario_inicio': horario_inicio.strftime('%H:%M') if horario_inicio else None,
        'horario_fim': horario_fim.strftime('%H:%M') if horario_fim else None,
        'logo_url': lanchonete.logo.url if lanchonete.logo else None
    }

    return JsonResponse(data)