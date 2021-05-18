# Generated by Django 3.2.3 on 2021-05-18 03:44

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_note_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='color',
            field=colorfield.fields.ColorField(choices=[('#E06C75', 'RED'), ('#E5C07B', 'YELLOW'), ('#98C379', 'GREEN'), ('#61AFEF', 'BLUE'), ('#ECECEC', 'DEFAULT')], default='#ECECEC', max_length=18),
        ),
    ]