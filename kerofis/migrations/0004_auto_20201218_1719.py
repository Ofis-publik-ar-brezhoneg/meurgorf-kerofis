# Generated by Django 3.1.1 on 2020-12-18 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kerofis', '0003_update_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phonetictranscriptionlink',
            name='link',
            field=models.FileField(db_column='kde_distagadur_enrolladenn', max_length=30, upload_to=''),
        ),
        migrations.AlterField(
            model_name='phonetictranscriptionlink',
            name='phonetic_transcription',
            field=models.ForeignKey(db_column='kde_niv', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='links', to='kerofis.phonetictranscription'),
        ),
    ]
