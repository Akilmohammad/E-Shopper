# Generated by Django 3.1.2 on 2020-11-28 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0018_auto_20201128_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='men_accessories',
            name='men_acc_image1',
            field=models.ImageField(default='plus.png', upload_to='men_acc/'),
        ),
        migrations.AlterField(
            model_name='men_accessories',
            name='men_acc_image2',
            field=models.ImageField(default='plus.png', upload_to='men_acc/'),
        ),
        migrations.AlterField(
            model_name='men_accessories',
            name='men_acc_image3',
            field=models.ImageField(default='plus.png', upload_to='men_acc/'),
        ),
    ]