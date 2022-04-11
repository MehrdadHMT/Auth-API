# Generated by Django 4.0.3 on 2022-04-11 07:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=11, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '09xxxxxxxxx'. Up to 15 digits allowed.", regex='^(?:0|98|\\+98|\\+980|0098|098|00980)?(9\\d{9})$')]),
        ),
    ]
