from django.db import models

class Lanchonete(models.Model):
    nome = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    endereco = models.CharField(max_length=255)
    
    # Horários de funcionamento por dia
    horario_segunda_inicio = models.TimeField(blank=True, null=True)
    horario_segunda_fim = models.TimeField(blank=True, null=True)
    
    horario_terca_inicio = models.TimeField(blank=True, null=True)
    horario_terca_fim = models.TimeField(blank=True, null=True)
    
    horario_quarta_inicio = models.TimeField(blank=True, null=True)
    horario_quarta_fim = models.TimeField(blank=True, null=True)
    
    horario_quinta_inicio = models.TimeField(blank=True, null=True)
    horario_quinta_fim = models.TimeField(blank=True, null=True)
    
    horario_sexta_inicio = models.TimeField(blank=True, null=True)
    horario_sexta_fim = models.TimeField(blank=True, null=True)
    
    horario_sabado_inicio = models.TimeField(blank=True, null=True)
    horario_sabado_fim = models.TimeField(blank=True, null=True)
    
    horario_domingo_inicio = models.TimeField(blank=True, null=True)
    horario_domingo_fim = models.TimeField(blank=True, null=True)
    
    telefone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nome