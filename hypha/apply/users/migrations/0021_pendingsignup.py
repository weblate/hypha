# Generated by Django 3.2.21 on 2023-09-12 08:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0020_auto_20230625_1825"),
    ]

    operations = [
        migrations.CreateModel(
            name="PendingSignup",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("token", models.CharField(max_length=255, unique=True)),
            ],
            options={
                "verbose_name_plural": "Pending signups",
                "ordering": ("created",),
            },
        ),
    ]
