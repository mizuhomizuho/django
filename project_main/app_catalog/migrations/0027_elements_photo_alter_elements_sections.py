# Generated by Django 4.2 on 2024-09-29 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_catalog', '0026_delete_table1_delete_table2_alter_elements_sections_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='elements',
            name='photo',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='elements_photos/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='elements',
            name='sections',
            field=models.ManyToManyField(blank=True, to='app_catalog.sections'),
        ),
    ]
