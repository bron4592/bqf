# Generated by Django 2.1.5 on 2019-03-07 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('structures', '0005_auto_20190306_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='struct',
            name='direction',
            field=models.CharField(default='Downtrend', max_length=100),
            preserve_default=False,
        ),
    ]
