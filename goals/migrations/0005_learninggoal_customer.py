# Generated by Django 3.1.5 on 2021-01-10 17:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("goals", "0004_auto_20210110_1659"),
    ]

    operations = [
        migrations.AddField(
            model_name="learninggoal",
            name="customer",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="goals.profile",
            ),
        ),
    ]
