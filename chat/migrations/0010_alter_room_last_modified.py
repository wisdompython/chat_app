# Generated by Django 5.0.2 on 2024-03-17 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0009_room_last_modified_alter_message_sender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='last_modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]