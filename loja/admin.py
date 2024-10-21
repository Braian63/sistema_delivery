from django.contrib import admin
from .models import Lanchonete

# Registrar o modelo Lanchonete no admin
@admin.register(Lanchonete)
class LanchoneteAdmin(admin.ModelAdmin):
    # Opcional: Lista de campos a serem exibidos na listagem do admin
    list_display = ('nome', 'endereco', 'telefone', 'email')

    # Opcional: Campos que serão pesquisáveis
    search_fields = ('nome', 'endereco', 'telefone')

    # Opcional: Exibir filtros laterais
    list_filter = ('nome',)

    # Opcional: Configuração dos campos editáveis no formulário de edição
    fieldsets = (
        ('Informações Gerais', {
            'fields': ('nome', 'logo', 'endereco', 'telefone', 'email'),
        }),
        ('Horários de Funcionamento', {
            'fields': (
                'horario_segunda_inicio', 'horario_segunda_fim',
                'horario_terca_inicio', 'horario_terca_fim',
                'horario_quarta_inicio', 'horario_quarta_fim',
                'horario_quinta_inicio', 'horario_quinta_fim',
                'horario_sexta_inicio', 'horario_sexta_fim',
                'horario_sabado_inicio', 'horario_sabado_fim',
                'horario_domingo_inicio', 'horario_domingo_fim',
            ),
        }),
    )
