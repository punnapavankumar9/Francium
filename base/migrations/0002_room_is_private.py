# Generated by Django 4.0.1 on 2022-02-09 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
    ]