# Generated by Django 2.2.7 on 2020-05-02 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventhandler', '0004_remove_event_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='author',
            field=models.OneToOneField(default=None, on_delete='CASCADE', to='eventhandler.User'),
        ),
    ]
