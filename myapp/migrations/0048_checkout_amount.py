# Generated by Django 3.1.2 on 2020-12-04 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0047_auto_20201204_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]