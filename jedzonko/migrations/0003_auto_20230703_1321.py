# Generated by Django 2.2.6 on 2023-07-03 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jedzonko', '0002_auto_20230630_1827'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='descritpion_preparing',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dayname',
            name='name',
            field=models.IntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')]),
        ),
    ]
