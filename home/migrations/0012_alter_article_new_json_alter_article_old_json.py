# Generated by Django 4.2.4 on 2023-09-14 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_article_new_json_article_old_json'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='new_json',
            field=models.TextField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='old_json',
            field=models.TextField(blank=True, default=dict, null=True),
        ),
    ]
