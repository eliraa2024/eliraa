# Generated by Django 5.0.2 on 2024-04-01 22:20

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quart', '0005_liraboletim_id_boletim_liraboletimdado_id_dado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='liraboletim',
            name='id',
        ),
        migrations.RemoveField(
            model_name='liraboletimdado',
            name='id',
        ),
        migrations.AlterField(
            model_name='liraboletim',
            name='id_boletim',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='liraboletimdado',
            name='id_dado',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
