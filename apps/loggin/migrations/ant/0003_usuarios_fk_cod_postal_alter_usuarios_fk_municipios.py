# Generated by Django 5.1.7 on 2025-03-11 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("loggin", "0002_alter_usuarios_sexo"),
    ]

    operations = [
        migrations.AddField(
            model_name="usuarios",
            name="fk_cod_postal",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="usuarios",
            name="fk_municipios",
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
