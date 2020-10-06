# Generated by Django 3.1.1 on 2020-09-23 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meurgorf', '0003_usage_and_phonetic'),
    ]

    operations = [
        migrations.CreateModel(
            name='TermSearchQuery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField(db_column='me_reket', max_length=200, null=None, unique=True)),
                ('date', models.DateTimeField()),
                ('counter', models.IntegerField(db_column='me_konter_goulenn', null=None)),
                ('results_number', models.IntegerField(db_column='me_konter_disoch', null=None)),
            ],
            options={
                'db_table': 'meurgorf_enklaskou',
            },
        ),
    ]