# Generated by Django 4.2 on 2024-09-12 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_alter_user_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="image_field",
            field=models.ImageField(default="static/default", upload_to=""),
        ),
    ]
