# Generated by Django 3.1.1 on 2020-09-23 07:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commun', '0002_auto_20200828_1007'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['abbrevation'], 'verbose_name': 'Oberenn'},
        ),
    ]