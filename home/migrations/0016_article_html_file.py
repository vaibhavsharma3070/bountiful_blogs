# Generated by Django 4.2.4 on 2023-10-05 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_alter_reviewlogs_modelname'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='html_file',
            field=models.FileField(blank=True, null=True, upload_to='media/'),
        ),
    ]
