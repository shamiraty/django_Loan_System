# Generated by Django 4.2.9 on 2024-01-18 18:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("debt", "0009_monthlyweatherbycity"),
    ]

    operations = [
        migrations.DeleteModel(
            name="MonthlyWeatherByCity",
        ),
    ]