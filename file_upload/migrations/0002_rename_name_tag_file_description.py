# Generated by Django 3.2.13 on 2023-03-24 03:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('file_upload', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='file',
            old_name='name_tag',
            new_name='description',
        ),
    ]