# Generated by Django 4.2.6 on 2023-11-20 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_profile_list_allergens_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='list_own_recipes',
            field=models.JSONField(default=dict),
        ),
    ]
