# Generated by Django 3.1.2 on 2020-11-28 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0024_auto_20201128_1245'),
    ]

    operations = [
        migrations.AddField(
            model_name='women_cloth',
            name='women_cloth_proID',
            field=models.CharField(default='', max_length=100),
        ),
    ]