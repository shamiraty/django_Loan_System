# Generated by Django 4.2.9 on 2024-01-21 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("debt", "0019_alter_target_amount"),
    ]

    operations = [
        migrations.AlterField(
            model_name="target",
            name="Amount",
            field=models.FloatField(default=100000),
        ),
    ]
