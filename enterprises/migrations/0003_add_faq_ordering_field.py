# Generated by Django 4.2.4 on 2023-08-31 00:14

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("enterprises", "0002_frequentlyaskedquestion"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="frequentlyaskedquestion",
            options={"ordering": ["ordering"]},
        ),
    ]