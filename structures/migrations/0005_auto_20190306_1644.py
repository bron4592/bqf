# Generated by Django 2.1.5 on 2019-03-06 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('structures', '0004_auto_20190305_2230'),
    ]

    operations = [
        migrations.AddField(
            model_name='struct',
            name='abLength',
            field=models.FloatField(default=12),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='struct',
            name='c',
            field=models.FloatField(default=12),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='struct',
            name='takeout',
            field=models.FloatField(default=12),
            preserve_default=False,
        ),
    ]
