# Generated by Django 5.1.6 on 2025-04-21 21:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "tracker",
            "0006_alter_consumedfood_unique_together_consumedfood_log_and_more",
        ),
    ]

    operations = [
        migrations.DeleteModel(
            name="FoodHistory",
        ),
    ]
