# Generated by Django 4.1.7 on 2023-02-20 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cal", "0004_event_origin"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="external_id",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
