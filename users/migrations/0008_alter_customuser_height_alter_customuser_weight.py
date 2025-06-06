# Generated by Django 5.1.6 on 2025-03-03 17:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0007_alter_customuser_password"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="height",
            field=models.FloatField(
                validators=[django.core.validators.MinValueValidator(0.1)]
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="weight",
            field=models.FloatField(
                validators=[django.core.validators.MinValueValidator(0.1)]
            ),
        ),
    ]
