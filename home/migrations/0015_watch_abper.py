# Generated by Django 2.1.5 on 2019-03-15 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_auto_20190314_2339'),
    ]

    operations = [
        migrations.AddField(
            model_name='watch',
            name='abper',
            field=models.FloatField(default=0.3),
            preserve_default=False,
        ),
    ]