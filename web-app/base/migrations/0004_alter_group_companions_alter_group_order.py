# Generated by Django 4.2.9 on 2024-01-30 02:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_ride_ride_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='companions',
            field=models.ManyToManyField(blank=True, null=True, related_name='participated_group', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='group',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group_order', to='base.ride'),
        ),
    ]