# Generated by Django 4.2 on 2024-09-26 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_catalog', '0009_alter_tree_code'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='tree',
            name='app_catalog_code_d4c480_idx',
        ),
        migrations.AlterField(
            model_name='tree',
            name='code',
            field=models.CharField(db_index=True, max_length=255),
        ),
    ]
