# Generated by Django 2.1.5 on 2019-04-09 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('structures', '0019_struct_b'),
    ]

    operations = [
        migrations.AddField(
            model_name='struct',
            name='newTake',
            field=models.BooleanField(default=False),
        ),
    ]