# Generated by Django 5.0 on 2024-01-04 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('titiksurvei', '0005_survei_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survei',
            name='image',
            field=models.ImageField(default=models.CharField(), upload_to='fotosurvei/'),
        ),
    ]
