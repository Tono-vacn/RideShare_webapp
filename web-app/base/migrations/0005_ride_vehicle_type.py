# Generated by Django 4.2.9 on 2024-01-30 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_group_companions_alter_group_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='ride',
            name='vehicle_type',
            field=models.CharField(blank=True, choices=[('Economy', 'Economy'), ('Comfort', 'Comfort'), ('Large', 'Large'), ('XL', 'XL')], default='Economy', max_length=20, null=True),
        ),
    ]
