# Generated by Django 4.2.4 on 2023-09-12 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_batch_alter_article_batch'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='new_article',
            field=models.FileField(blank=True, null=True, upload_to='new_articles/'),
        ),
        migrations.AddField(
            model_name='article',
            name='old_article',
            field=models.FileField(blank=True, null=True, upload_to='old_articles/'),
        ),
    ]
