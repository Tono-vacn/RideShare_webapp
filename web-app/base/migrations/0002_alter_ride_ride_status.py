# Generated by Django 4.2.9 on 2024-01-29 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='ride_status',
            field=models.CharField(choices=[('Open', 'OPEN'), ('Cancelled', 'CANCELLED'), ('Comfirmed', 'COMFIRMED'), ('In Progress', 'PROGRESS'), ('Completed', 'COMPLETED')], default='OPEN', max_length=15),
        ),
    ]