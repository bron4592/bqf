# Generated by Django 2.1.5 on 2019-02-19 23:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='struct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idCode', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('exchange', models.CharField(max_length=100)),
                ('eqName', models.CharField(max_length=100)),
                ('timeFrame', models.CharField(max_length=100)),
                ('retracePer', models.DecimalField(decimal_places=2, max_digits=3)),
                ('potReturnPer', models.DecimalField(decimal_places=2, max_digits=3)),
                ('perRemain', models.DecimalField(decimal_places=2, max_digits=3)),
                ('bVol', models.IntegerField()),
                ('takeVol', models.IntegerField()),
                ('volDelt', models.IntegerField()),
                ('dateEnd', models.DateField()),
                ('valid', models.BooleanField()),
                ('author', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
