# Generated by Django 5.2.3 on 2025-07-01 13:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("edu_materials", "0003_subscription"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lesson",
            name="course",
            field=models.ForeignKey(
                help_text="выберите курс",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="lessons",
                to="edu_materials.course",
                verbose_name="курс",
            ),
        ),
    ]
