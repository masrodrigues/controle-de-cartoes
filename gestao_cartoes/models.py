# models.py
from django.db import models


class Cartao(models.Model):
    nome = models.CharField(max_length=100)
    limite = models.DecimalField(max_digits=10, decimal_places=2)
    vencimento = models.IntegerField()
    imagem = models.ImageField(upload_to='imagens_cartoes/', default='imagens_cartoes/default_image.jpg')

    def __str__(self):
        return self.nome
class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

from django.db import models
from datetime import timedelta
# Certifique-se de importar os modelos Cartao e Categoria corretamente

class Gasto(models.Model):
    cartao = models.ForeignKey(Cartao, on_delete=models.CASCADE, related_name='gastos')
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    descricao = models.CharField(max_length=255)
    parcelas = models.IntegerField(default=1)

    def __str__(self):
        return self.descricao