# Generated by Django 4.2.9 on 2024-01-19 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("debt", "0013_remove_customer_addedby_remove_customer_employeeid"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customer",
            name="Document",
        ),
        migrations.RemoveField(
            model_name="customer",
            name="Passport",
        ),
    ]
