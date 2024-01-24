# Generated by Django 4.2.9 on 2024-01-24 04:19

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_user_managers_alter_user_username'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(default='NULL', help_text='User Name', max_length=64),
        ),
    ]
