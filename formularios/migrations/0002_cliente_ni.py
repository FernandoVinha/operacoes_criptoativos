# Generated by Django 5.0.6 on 2024-06-07 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formularios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='ni',
            field=models.CharField(blank=True, help_text='Número de identificação adicional do cliente (opcional).', max_length=30, null=True),
        ),
    ]