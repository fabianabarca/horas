# Generated by Django 4.0.5 on 2022-09-15 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enPapelera', models.BooleanField(default='False')),
                ('fechaPapelera', models.DateField(blank=True, null=True)),
                ('fechaCreacion', models.DateField(auto_now_add=True, null=True)),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
