# Generated by Django 3.2 on 2024-06-08 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_auto_20240608_1130'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rewardoffering',
            old_name='TotalZhibi',
            new_name='Zhibi',
        ),
    ]
