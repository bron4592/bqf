# Generated by Django 2.1.5 on 2019-04-09 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0030_auto_20190408_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watch',
            name='abPer',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='watch',
            name='perRemain',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='watch',
            name='retracePer',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='watch',
            name='volDelt',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]