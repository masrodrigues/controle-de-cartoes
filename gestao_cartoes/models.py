from django.db import models
from datetime import timedelta

class Cartao(models.Model):
    nome = models.CharField(max_length=100)
    limite = models.DecimalField(max_digits=10, decimal_places=2, help_text="Limite máximo do cartão.")
    vencimento = models.IntegerField(help_text="Dia do vencimento (1 a 31).")
    imagem = models.ImageField(
        upload_to='imagens_cartoes/', 
        default='imagens_cartoes/default_image.jpg',
        help_text="Imagem opcional do cartão."
    )

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']
        verbose_name = "Cartão"
        verbose_name_plural = "Cartões"

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True, help_text="Nome da categoria única.")

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

class Gasto(models.Model):
    cartao = models.ForeignKey(
        Cartao, 
        on_delete=models.CASCADE, 
        related_name='gastos', 
        help_text="Cartão associado ao gasto."
    )
    valor = models.DecimalField(max_digits=10, decimal_places=2, help_text="Valor do gasto.")
    data = models.DateField(help_text="Data em que o gasto foi realizado.")
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='gastos',
        help_text="Categoria opcional do gasto."
    )
    descricao = models.CharField(max_length=255, help_text="Descrição detalhada do gasto.")
    parcelas = models.IntegerField(default=1, help_text="Número de parcelas (mínimo 1).")

    def __str__(self):
        return f"{self.descricao} - {self.valor} ({self.data})"

    class Meta:
        ordering = ['-data']
        verbose_name = "Gasto"
        verbose_name_plural = "Gastos"
