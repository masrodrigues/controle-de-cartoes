# Generated by Django 5.0.6 on 2024-07-06 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestao_cartoes', '0009_remove_gasto_pago'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartao',
            name='pago',
            field=models.BooleanField(default=False),
        ),
    ]
