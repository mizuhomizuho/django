# Generated by Django 4.2 on 2024-09-26 08:22

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('app_catalog', '0011_alter_tree_code'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Tree',
            new_name='Catalog',
        ),
        migrations.AlterModelManagers(
            name='catalog',
            managers=[
                ('tree', django.db.models.manager.Manager()),
            ],
        ),
    ]
