# Generated by Django 4.2.6 on 2023-10-20 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vessel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vessel',
            name='vessel_schedule',
            field=models.TextField(blank=True, null=True),
        ),
    ]
