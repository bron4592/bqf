# Generated by Django 2.1.5 on 2019-03-21 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0023_auto_20190320_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hot',
            name='value1',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='hot',
            name='value2',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='hot',
            name='value3',
            field=models.IntegerField(),
        ),
    ]
