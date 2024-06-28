# models.py
from django.db import models

class Cartao(models.Model):
    nome = models.CharField(max_length=100)
    limite = models.DecimalField(max_digits=10, decimal_places=2)
    vencimento = models.IntegerField()  # Garanta que este campo exista e esteja correto

    def __str__(self):
        return self.nome

class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Gasto(models.Model):
    cartao = models.ForeignKey(Cartao, on_delete=models.CASCADE, related_name='gastos')
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    descricao = models.CharField(max_length=255)  # Adicionando o campo descricao

    def __str__(self):
        return self.descricao

    def __str__(self):
        return self.descricao