# Generated by Django 5.0.1 on 2024-01-14 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Department",
            fields=[
                ("DepartmentName", models.CharField(max_length=250)),
                ("HeadOfDepartment", models.CharField(max_length=250)),
                ("RegisteredDate", models.DateTimeField(auto_now_add=True)),
                (
                    "DepartmentId",
                    models.CharField(max_length=250, primary_key=True, serialize=False),
                ),
            ],
        ),
    ]