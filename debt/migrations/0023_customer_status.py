# Generated by Django 4.2.9 on 2024-01-21 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("debt", "0022_alter_customer_nationalid"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="Status",
            field=models.CharField(
                choices=[
                    ("Approved", "Approved"),
                    ("Pending", "Pending"),
                    ("Rejected", "Rejected"),
                ],
                default="Pending",
                max_length=50,
                null=True,
            ),
        ),
    ]