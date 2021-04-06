# Generated by Django 3.1.6 on 2021-02-21 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0003_auto_20210221_2212'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_agent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_organizer',
            field=models.BooleanField(default=True),
        ),
    ]
