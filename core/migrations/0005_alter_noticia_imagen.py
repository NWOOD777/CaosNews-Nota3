# Generated by Django 5.0.6 on 2024-05-25 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_noticia_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticia',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='noticias'),
        ),
    ]
