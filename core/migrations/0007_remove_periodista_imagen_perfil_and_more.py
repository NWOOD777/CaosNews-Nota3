# Generated by Django 5.0.6 on 2024-05-27 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_periodista_imagen_perfil'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='periodista',
            name='Imagen_Perfil',
        ),
        migrations.AddField(
            model_name='periodista',
            name='imagen_perfil',
            field=models.ImageField(blank=True, null=True, upload_to='noticias'),
        ),
    ]