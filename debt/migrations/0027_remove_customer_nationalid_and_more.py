# Generated by Django 4.2.9 on 2024-01-21 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("debt", "0026_alter_loan_loanstatus"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customer",
            name="NationalID",
        ),
        migrations.RemoveField(
            model_name="customer",
            name="PassportSize",
        ),
        migrations.AlterField(
            model_name="loan",
            name="Status",
            field=models.CharField(
                choices=[
                    ("Rejected", "Rejected"),
                    ("Pending", "Pending"),
                    ("Approved", "Approved"),
                ],
                default="Pending",
                max_length=50,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="loan",
            name="loanStatus",
            field=models.CharField(
                choices=[("Not Active", "Not Active"), ("Active", "Active")],
                default="Active",
                max_length=50,
                null=True,
            ),
        ),
    ]
