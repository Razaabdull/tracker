# Generated by Django 4.2.3 on 2023-08-24 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_user_income_purpose'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
