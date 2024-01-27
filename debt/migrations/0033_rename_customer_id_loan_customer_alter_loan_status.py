# Generated by Django 4.2.9 on 2024-01-21 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("debt", "0032_rename_customer_loan_customer_id_alter_loan_status_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="loan",
            old_name="Customer_id",
            new_name="Customer",
        ),
        migrations.AlterField(
            model_name="loan",
            name="Status",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("Rejected", "Rejected"),
                    ("Approved", "Approved"),
                ],
                default="Pending",
                max_length=50,
                null=True,
            ),
        ),
    ]
