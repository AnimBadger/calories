# Generated by Django 4.2.5 on 2023-09-19 13:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_rename_user_id_caloriesinput_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caloriesinput',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username'),
        ),
    ]