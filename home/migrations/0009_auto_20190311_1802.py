# Generated by Django 2.1.5 on 2019-03-11 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20190311_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='search',
            name='specificEq',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
