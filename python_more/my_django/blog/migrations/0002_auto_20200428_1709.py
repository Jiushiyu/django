# Generated by Django 3.0.5 on 2020-04-28 09:09

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 28, 9, 9, 16, 813667, tzinfo=utc)),
        ),
    ]
