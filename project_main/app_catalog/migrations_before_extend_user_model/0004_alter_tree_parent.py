# Generated by Django 4.2 on 2024-09-24 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_catalog', '0003_remove_tree_active_tree_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tree',
            name='parent',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='app_catalog.tree'),
        ),
    ]
