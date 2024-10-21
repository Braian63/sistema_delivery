from django.db import models
from django.db import models
from datetime import datetime
from django.utils.safestring import mark_safe

class Categoria(models.Model):
    categoria = models.CharField(max_length=200)

    def __str__(self):
        return self.categoria

class Opcoes(models.Model):
    nome = models.CharField(max_length=100)
    acrecimo = models.FloatField(default=0)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Opções"
    def __str__(self):
        return self.nome

class Adicional(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    maximo = models.IntegerField()
    minimo = models.IntegerField()
    opcoes = models.ManyToManyField(Opcoes)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Adicionais"
    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome_produto = models.CharField(max_length=100)
    img = models.ImageField(upload_to='post_img')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    preco = models.FloatField()
    descricao = models.TextField()
    ingredientes = models.CharField(max_length=2000)
    adicionais = models.ManyToManyField(Adicional, blank=True)
    ativo = models.BooleanField(default=True)

    @mark_safe
    def icone(self):
        return f'<img width="30px" src="/media/{self.img}">'


    def __str__(self):
        return self.nome_produto
    

class Preco(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='precos')
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField(null=True, blank=True)  # Pode ser nulo se for o preço atual

    def __str__(self):
        return f"R$ {self.valor} - {self.produto.nome} (Válido de {self.data_inicio} até {self.data_fim or 'atualmente'})"

    def is_valido(self):
        """Verifica se o preço ainda é válido."""
        now = datetime.now()
        return self.data_fim is None or self.data_fim > now