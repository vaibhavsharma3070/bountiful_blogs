# Generated by Django 4.2.4 on 2023-10-04 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_reviewlogs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewlogs',
            name='modelname',
            field=models.CharField(max_length=100),
        ),
    ]