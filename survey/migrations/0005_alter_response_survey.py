# Generated by Django 5.0 on 2024-01-15 07:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0004_alter_survey_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='response',
            name='survey',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='response', to='survey.survey'),
        ),
    ]
