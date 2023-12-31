# Generated by Django 4.2.4 on 2023-09-07 11:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_settings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='image_folder',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.CreateModel(
            name='ProjectImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('parent_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.project')),
            ],
        ),
    ]
