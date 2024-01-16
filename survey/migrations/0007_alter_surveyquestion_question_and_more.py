# Generated by Django 5.0 on 2024-01-16 20:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0006_alter_response_submitted_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveyquestion',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='surveyquestion', to='survey.question'),
        ),
        migrations.AlterField(
            model_name='surveyquestion',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='surveyquestion', to='survey.survey'),
        ),
    ]
