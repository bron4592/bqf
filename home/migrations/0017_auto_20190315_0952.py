# Generated by Django 2.1.5 on 2019-03-15 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_remove_watch_cdleg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watch',
            name='specif',
            field=models.IntegerField(),
        ),
    ]
