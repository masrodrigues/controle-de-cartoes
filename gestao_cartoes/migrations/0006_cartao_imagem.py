# Generated by Django 5.0.6 on 2024-06-29 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestao_cartoes', '0005_gasto_parcelas'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartao',
            name='imagem',
            field=models.ImageField(default='path/to/default/image.jpg', upload_to='imagens_cartoes/'),
        ),
    ]
