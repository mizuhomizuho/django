# Generated by Django 4.2 on 2024-09-24 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_catalog', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tree',
            name='active',
        ),
        migrations.AddField(
            model_name='tree',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
