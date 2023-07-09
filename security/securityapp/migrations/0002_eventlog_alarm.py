# Generated by Django 4.2.3 on 2023-07-09 09:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("securityapp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="EventLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("event_type", models.CharField(max_length=50)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("details", models.TextField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Alarm",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("alarm_type", models.CharField(max_length=50)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("details", models.TextField()),
                (
                    "event_log",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="securityapp.eventlog",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
