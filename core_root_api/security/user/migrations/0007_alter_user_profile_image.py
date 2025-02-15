# Generated by Django 5.1.4 on 2025-02-08 08:29

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core_root_api_security_user", "0006_alter_user_profile_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="profile_image",
            field=cloudinary.models.CloudinaryField(
                blank=True, max_length=255, null=True, verbose_name="profile_image"
            ),
        ),
    ]
