# Generated by Django 5.0.6 on 2024-11-13 18:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestao_cartoes', '0011_remove_cartao_pago'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartao',
            options={'ordering': ['nome'], 'verbose_name': 'Cartão', 'verbose_name_plural': 'Cartões'},
        ),
        migrations.AlterModelOptions(
            name='categoria',
            options={'ordering': ['nome'], 'verbose_name': 'Categoria', 'verbose_name_plural': 'Categorias'},
        ),
        migrations.AlterModelOptions(
            name='gasto',
            options={'ordering': ['-data'], 'verbose_name': 'Gasto', 'verbose_name_plural': 'Gastos'},
        ),
        migrations.AlterField(
            model_name='cartao',
            name='imagem',
            field=models.ImageField(default='imagens_cartoes/default_image.jpg', help_text='Imagem opcional do cartão.', upload_to='imagens_cartoes/'),
        ),
        migrations.AlterField(
            model_name='cartao',
            name='limite',
            field=models.DecimalField(decimal_places=2, help_text='Limite máximo do cartão.', max_digits=10),
        ),
        migrations.AlterField(
            model_name='cartao',
            name='vencimento',
            field=models.IntegerField(help_text='Dia do vencimento (1 a 31).'),
        ),
        migrations.AlterField(
            model_name='categoria',
            name='nome',
            field=models.CharField(help_text='Nome da categoria única.', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='gasto',
            name='cartao',
            field=models.ForeignKey(help_text='Cartão associado ao gasto.', on_delete=django.db.models.deletion.CASCADE, related_name='gastos', to='gestao_cartoes.cartao'),
        ),
        migrations.AlterField(
            model_name='gasto',
            name='categoria',
            field=models.ForeignKey(blank=True, help_text='Categoria opcional do gasto.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gastos', to='gestao_cartoes.categoria'),
        ),
        migrations.AlterField(
            model_name='gasto',
            name='data',
            field=models.DateField(help_text='Data em que o gasto foi realizado.'),
        ),
        migrations.AlterField(
            model_name='gasto',
            name='descricao',
            field=models.CharField(help_text='Descrição detalhada do gasto.', max_length=255),
        ),
        migrations.AlterField(
            model_name='gasto',
            name='parcelas',
            field=models.IntegerField(default=1, help_text='Número de parcelas (mínimo 1).'),
        ),
        migrations.AlterField(
            model_name='gasto',
            name='valor',
            field=models.DecimalField(decimal_places=2, help_text='Valor do gasto.', max_digits=10),
        ),
    ]