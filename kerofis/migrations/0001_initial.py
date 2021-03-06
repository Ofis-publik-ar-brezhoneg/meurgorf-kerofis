# Generated by Django 3.1.1 on 2020-10-22 10:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('commun', '0002_unaccent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_bre', models.CharField(db_column='kr_rummad_bre', max_length=50)),
                ('name_fra', models.CharField(db_column='kr_rummad_fra', max_length=50)),
            ],
            options={
                'db_table': 'kerofis_rummad',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insee_code', models.PositiveIntegerField(db_column='kkb_kod_insee')),
                ('postal_code', models.PositiveIntegerField(db_column='kkb_kod_post')),
                ('name_bre', models.CharField(db_column='kkb_kumun_bre', max_length=50)),
                ('name_fra', models.CharField(db_column='kkb_kumun_fra', max_length=50)),
            ],
            options={
                'db_table': 'kerofis_kumun_breizh',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_column='kd_departamant_niv', max_length=2)),
                ('name_bre', models.CharField(db_column='kd_departamant_bre', max_length=30)),
                ('name_fra', models.CharField(db_column='kd_departamant_fra', max_length=30)),
            ],
            options={
                'db_table': 'kerofis_departamant',
            },
        ),
        migrations.CreateModel(
            name='Informant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(db_column='kt_anv_bihan_titourer', max_length=100, null=True)),
                ('last_name', models.CharField(db_column='kt_anv_titourer', max_length=200, null=True)),
                ('surname', models.CharField(db_column='kt_lesanv', max_length=50, null=True)),
                ('occupation', models.CharField(db_column='kt_micher', max_length=200, null=True)),
                ('birthdate', models.CharField(db_column='kt_bloaz_ganedigezh', max_length=4)),
                ('birthplace', models.CharField(db_column='kt_lech_ganedigezh', max_length=50, null=True)),
                ('cities', models.CharField(db_column='kt_kumun_titouret', max_length=250, null=True)),
                ('arrival_date', models.CharField(db_column='kt_pegoulz_er_gumun', max_length=4, null=True)),
                ('notes', models.TextField(db_column='kt_notenn', null=True)),
                ('contact', models.TextField(db_column='kt_darempred', null=True)),
                ('old_id', models.IntegerField(null=True)),
                ('interviewed_by', models.ForeignKey(db_column='kt_enklasker', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'kerofis_titourer',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='kk_anv', max_length=255)),
                ('on_ign', models.BooleanField(db_column='kk_ign')),
                ('ign_date', models.DateField(db_column='kk_deiziad_ign', null=True)),
                ('formalized_date', models.DateField(db_column='kk_deiziad_ofisielisaet', null=True)),
                ('is_public', models.BooleanField(db_column='kk_aotre_embann')),
                ('generic_name', models.CharField(db_column='kk_stagadenn', max_length=255)),
                ('on_bf', models.BooleanField(db_column='kk_kartenn_bf')),
                ('reference', models.TextField(db_column='kk_daveenn')),
                ('notes', models.TextField(db_column='kk_notenn_studi')),
                ('formalized_proposal', models.CharField(blank=True, db_column='kk_kinnig_skoueriekaat', max_length=120, null=True)),
                ('proposal_author', models.TextField(db_column='kk_goulenner')),
                ('square_bf', models.CharField(db_column='kk_karrezenn', max_length=5)),
                ('longitude', models.DecimalField(blank=True, db_column='kk_daveenn_douaroniel_lg', decimal_places=16, max_digits=22, null=True)),
                ('latitude', models.DecimalField(blank=True, db_column='kk_daveenn_douaroniel_lt', decimal_places=16, max_digits=22, null=True)),
                ('etymological_note_bre', models.TextField(db_column='kk_gerdarzh_bre')),
                ('etymological_note_fra', models.TextField(db_column='kk_gerdarzh_fra')),
                ('created_at', models.DateTimeField(db_column='kk_deiziad_ebarzhin', default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(null=True)),
                ('old_id', models.IntegerField(null=True)),
                ('category', models.ForeignKey(db_column='kk_rummad', null=True, on_delete=django.db.models.deletion.SET_NULL, to='kerofis.category')),
                ('city', models.ForeignKey(db_column='kk_kumun', null=True, on_delete=django.db.models.deletion.SET_NULL, to='kerofis.city')),
                ('created_by', models.ForeignKey(db_column='kk_aozer_ar_fichenn', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='locations', to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(db_column='kk_departamant', null=True, on_delete=django.db.models.deletion.SET_NULL, to='kerofis.department')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'kerofis_kreiz',
            },
        ),
        migrations.CreateModel(
            name='PhoneticTranscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phonetic_transcription', models.CharField(db_column='kd_distagadur', max_length=255)),
                ('is_standard', models.BooleanField(db_column='kd_distagadur_skouer', default=False)),
                ('created_at', models.CharField(db_column='kd_deziad', max_length=10, null=True)),
                ('informant', models.ForeignKey(db_column='kd_titourer', null=True, on_delete=django.db.models.deletion.SET_NULL, to='kerofis.informant')),
                ('location', models.ForeignKey(db_column='kd_niv', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='phonetic_transcriptions', to='kerofis.location')),
            ],
            options={
                'db_table': 'kerofis_distagadur',
            },
        ),
        migrations.CreateModel(
            name='TermSearchQuery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField(db_column='ke_goulenn', max_length=200, null=None, unique=True)),
                ('query_type', models.CharField(db_column='ke_oberataer', max_length=2, null=None)),
                ('date', models.DateTimeField(db_column='ke_deiziad')),
                ('counter', models.IntegerField(db_column='ke_konter_reket', null=None)),
                ('results_number', models.IntegerField(db_column='ke_konter_disoch', null=None)),
            ],
            options={
                'db_table': 'kerofis_enklaskou',
            },
        ),
        migrations.CreateModel(
            name='StandardizedForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('standardized_form', models.CharField(db_column='kss_dibab', max_length=100)),
                ('date', models.DateField(db_column='kss_deiziad_degemer', null=True)),
                ('location', models.ForeignKey(db_column='kss_niv', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='standardized_form', to='kerofis.location')),
            ],
            options={
                'db_table': 'kerofis_stumm_skouer',
            },
        ),
        migrations.CreateModel(
            name='PhoneticTranscriptionLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(db_column='kde_distagadur_enrolladenn', max_length=30)),
                ('phonetic_transcription', models.ForeignKey(db_column='kde_niv', null=True, on_delete=django.db.models.deletion.SET_NULL, to='kerofis.phonetictranscription')),
            ],
            options={
                'db_table': 'kerofis_distagadur_enrolladenn',
            },
        ),
        migrations.CreateModel(
            name='OtherForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usage_form', models.CharField(db_column='ksa_stumm', max_length=100)),
                ('litteral_year', models.CharField(db_column='ksa_bloavezh', max_length=12)),
                ('year', models.PositiveSmallIntegerField(db_column='ksa_bloavezh_niverel', null=True)),
                ('reference', models.TextField(db_column='ksa_daveenn')),
                ('book', models.ForeignKey(db_column='ksa_mammenn', null=True, on_delete=django.db.models.deletion.SET_NULL, to='commun.book')),
                ('location', models.ForeignKey(db_column='ksa_niv', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='other_forms', to='kerofis.location')),
            ],
            options={
                'db_table': 'kerofis_stumm_all',
            },
        ),
        migrations.CreateModel(
            name='OldForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_form', models.CharField(db_column='ksk_stumm', max_length=100)),
                ('litteral_year', models.CharField(db_column='ksk_bloavezh', max_length=30)),
                ('year', models.PositiveSmallIntegerField(db_column='ksk_bloavezh_niverel', null=True)),
                ('reference', models.TextField(db_column='ksk_daveenn')),
                ('book', models.ForeignKey(db_column='ksk_mammenn', null=True, on_delete=django.db.models.deletion.SET_NULL, to='commun.book')),
                ('location', models.ForeignKey(db_column='ksk_niv', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='old_forms', to='kerofis.location')),
            ],
            options={
                'db_table': 'kerofis_stumm_kozh',
            },
        ),
        migrations.AddField(
            model_name='city',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='kerofis.department'),
        ),
        migrations.CreateModel(
            name='AttestedForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attested_form', models.CharField(db_column='kst_stumm', max_length=80, null=True)),
                ('is_labeled', models.BooleanField(db_column='kst_stumm_skouer', default=True)),
                ('litteral_year', models.CharField(db_column='kst_bloavezh', max_length=10)),
                ('year', models.PositiveSmallIntegerField(db_column='kst_bloavezh_niverel', null=True)),
                ('reference', models.TextField(db_column='kst_daveenn')),
                ('book', models.ForeignKey(db_column='kst_mammenn', null=True, on_delete=django.db.models.deletion.SET_NULL, to='commun.book')),
                ('location', models.ForeignKey(db_column='kst_niv', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='attested_forms', to='kerofis.location')),
            ],
            options={
                'db_table': 'kerofis_stumm_testeniekaet',
            },
        ),
    ]
