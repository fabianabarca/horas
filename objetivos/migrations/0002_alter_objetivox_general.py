# Generated by Django 4.1.1 on 2022-10-06 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("objetivos", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="objetivox",
            name="general",
            field=models.BooleanField(verbose_name="¿Es objetivo general?"),
        ),
    ]