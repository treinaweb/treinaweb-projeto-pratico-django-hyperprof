# Generated by Django 4.2.3 on 2023-07-10 18:53

from django.db import migrations, models
import teachers.models


class Migration(migrations.Migration):
    dependencies = [
        ("teachers", "0002_teacher_profile_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="teacher",
            name="profile_image",
            field=models.ImageField(
                null=True, upload_to=teachers.models.get_unique_filename
            ),
        ),
    ]
