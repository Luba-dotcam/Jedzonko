# Generated by Django 2.2.6 on 2023-07-03 11:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jedzonko', '0003_auto_20230703_1321'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='descritpion_preparing',
            new_name='description_preparing',
        ),
    ]
