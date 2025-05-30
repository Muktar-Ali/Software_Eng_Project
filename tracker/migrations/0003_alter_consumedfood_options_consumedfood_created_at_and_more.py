# Generated by Django 5.1.6 on 2025-04-18 00:17

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_alter_consumedfood_date_consumed'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='consumedfood',
            options={'ordering': ['-date_consumed', '-created_at'], 'verbose_name': 'Consumed Food', 'verbose_name_plural': 'Consumed Foods'},
        ),
        migrations.AddField(
            model_name='consumedfood',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Creation Time'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='consumedfood',
            name='date_consumed',
            field=models.DateField(verbose_name='Date Consumed'),
        ),
        migrations.AlterField(
            model_name='consumedfood',
            name='fatsecret_food_id',
            field=models.CharField(max_length=50, verbose_name='FatSecret Food ID'),
        ),
        migrations.AlterField(
            model_name='consumedfood',
            name='servings',
            field=models.FloatField(default=1.0, validators=[django.core.validators.MinValueValidator(0.1)], verbose_name='Servings Consumed'),
        ),
        migrations.AlterField(
            model_name='consumedfood',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterUniqueTogether(
            name='consumedfood',
            unique_together={('user', 'fatsecret_food_id', 'date_consumed')},
        ),
    ]
