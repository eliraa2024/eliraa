# Generated by Django 5.0.2 on 2024-04-25 13:57

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("quart", "0011_alter_indice_bairro_nome"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="liraboletim",
            options={"ordering": ["-created_at"]},
        ),
    ]