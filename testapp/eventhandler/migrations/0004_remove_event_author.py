# Generated by Django 2.2.7 on 2020-05-02 12:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventhandler', '0003_auto_20200502_1144'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='author',
        ),
    ]
