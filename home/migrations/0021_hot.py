# Generated by Django 2.1.5 on 2019-03-20 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_remove_watch_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='hot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotName', models.CharField(max_length=100)),
                ('indicator1', models.CharField(max_length=100)),
                ('timeFrame1', models.CharField(max_length=100)),
                ('indicator2', models.CharField(max_length=100)),
                ('timeFrame2', models.CharField(max_length=100)),
                ('indicator3', models.CharField(max_length=100)),
                ('timeFrame3', models.CharField(max_length=100)),
            ],
        ),
    ]
