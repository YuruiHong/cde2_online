# Generated by Django 3.2.13 on 2023-03-24 02:10

from django.db import migrations, models
import file_upload.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(null=True, upload_to=file_upload.models.user_directory_path)),
                ('name_tag', models.CharField(max_length=40, null=True)),
                ('contributor', models.CharField(max_length=20)),
            ],
        ),
    ]