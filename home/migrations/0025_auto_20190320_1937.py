# Generated by Django 2.1.5 on 2019-03-21 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0024_auto_20190320_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hot',
            name='value1',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='hot',
            name='value2',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='hot',
            name='value3',
            field=models.FloatField(),
        ),
    ]