# Generated by Django 5.0.2 on 2024-02-13 17:04

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_alter_privatemessage_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='privatemessage',
            options={'ordering': ['timestamp']},
        ),
        migrations.AlterField(
            model_name='privaterooms',
            name='room_name',
            field=models.UUIDField(default=uuid.UUID('a7ddf93b-4dfb-481e-95b0-11b30ebaff7b'), unique=True),
        ),
    ]