# Generated by Django 5.0 on 2024-01-04 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('titiksurvei', '0004_alter_survei_frame_filename'),
    ]

    operations = [
        migrations.AddField(
            model_name='survei',
            name='image',
            field=models.ImageField(default='path/to/default/image.jpg', upload_to='fotosurvei/'),
        ),
    ]
