# Generated by Django 5.0.2 on 2024-04-13 20:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quart', '0010_ciclo_liraboletim_ciclo_indice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indice',
            name='bairro_nome',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='bairros', to='quart.bairro'),
        ),
    ]
