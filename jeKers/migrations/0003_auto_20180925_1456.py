# Generated by Django 2.1.1 on 2018-09-25 13:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeKers', '0002_logs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logs',
            name='log_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]