# Generated by Django 5.0.6 on 2024-07-06 00:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestao_cartoes', '0008_gasto_pago'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gasto',
            name='pago',
        ),
    ]