# Generated by Django 4.1 on 2022-10-05 23:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_message_body_alter_message_subject'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['created']},
        ),
    ]
