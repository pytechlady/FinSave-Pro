# Generated by Django 5.0.3 on 2024-07-12 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0003_user_account_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='account_number',
            field=models.IntegerField(null=True, unique=True),
        ),
    ]