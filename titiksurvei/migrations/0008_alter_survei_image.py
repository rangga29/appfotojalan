# Generated by Django 5.0 on 2024-01-04 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('titiksurvei', '0007_alter_survei_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survei',
            name='image',
            field=models.ImageField(default='path/to/default/image.jpg', upload_to='fotosurvei/'),
        ),
    ]
