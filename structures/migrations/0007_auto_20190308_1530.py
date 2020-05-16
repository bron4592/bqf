# Generated by Django 2.1.5 on 2019-03-08 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('structures', '0006_struct_direction'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='struct',
            options={'ordering': ['-date']},
        ),
        migrations.AlterField(
            model_name='struct',
            name='perRemain',
            field=models.DecimalField(decimal_places=3, max_digits=4),
        ),
        migrations.AlterField(
            model_name='struct',
            name='potReturnPer',
            field=models.DecimalField(decimal_places=3, max_digits=4),
        ),
        migrations.AlterField(
            model_name='struct',
            name='retracePer',
            field=models.DecimalField(decimal_places=3, max_digits=4),
        ),
    ]