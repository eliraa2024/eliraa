# Generated by Django 5.0.2 on 2024-03-04 20:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quart', '0002_alter_quarteirao_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quarteirao',
            options={'ordering': ['numero'], 'verbose_name_plural': 'Quarteiroes'},
        ),
        migrations.AlterField(
            model_name='imovel',
            name='complemento',
            field=models.CharField(blank=True, max_length=6),
        ),
        migrations.AlterField(
            model_name='quarteirao',
            name='bairro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='bairro', to='quart.bairro'),
        ),
    ]