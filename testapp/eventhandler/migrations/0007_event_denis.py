# Generated by Django 2.2.7 on 2020-05-02 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventhandler', '0006_remove_event_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='denis',
            field=models.CharField(default='Denis', max_length=10),
        ),
    ]
