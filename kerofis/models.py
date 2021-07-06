from django.db import models
from django.utils.timezone import now


class Department(models.Model):
    class Meta:
        db_table = 'kerofis_departamant'

    code = models.CharField(max_length=2, db_column='kd_departamant_niv')
    name_bre = models.CharField(max_length=30, db_column='kd_departamant_bre')
    name_fra = models.CharField(max_length=30, db_column='kd_departamant_fra')


class City(models.Model):
    class Meta:
        db_table = 'kerofis_kumun_breizh'

    insee_code = models.PositiveIntegerField(db_column='kkb_kod_insee')
    postal_code = models.PositiveIntegerField(db_column='kkb_kod_post')
    department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)
    name_bre = models.CharField(max_length=50, db_column='kkb_kumun_bre')
    name_fra = models.CharField(max_length=50, db_column='kkb_kumun_fra')


class Category(models.Model):
    class Meta:
        db_table = 'kerofis_rummad'

    name_bre = models.CharField(max_length=50, db_column='kr_rummad_bre')
    name_fra = models.CharField(max_length=50, db_column='kr_rummad_fra')


class Location(models.Model):
    class Meta:
        db_table = 'kerofis_kreiz'

    name = models.CharField(max_length=255, db_column='kk_anv')
    on_ign = models.BooleanField(db_column='kk_ign', default=False)
    ign_date = models.DateField(null=True, blank=True, db_column='kk_deiziad_ign')
    formalized_date = models.DateField(null=True, blank=True, db_column='kk_deiziad_ofisielisaet')
    is_public = models.BooleanField(db_column='kk_aotre_embann', default=True)
    generic_name = models.CharField(max_length=255, db_column='kk_stagadenn')
    on_bf = models.BooleanField(db_column='kk_kartenn_bf', default=False)
    bf_date = models.DateField(null=True, blank=True, db_column='kk_deiziad_bf')
    city = models.ForeignKey(City, null=True, blank=True, on_delete=models.SET_NULL, related_name='locations', db_column='kk_kumun')
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL, db_column='kk_departamant')
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='locations',
                                 db_column='kk_rummad')
    reference = models.TextField(db_column='kk_daveenn', blank=True, default="")
    notes = models.TextField(db_column='kk_notenn_studi', blank=True, default="")
    formalized_proposal = models.CharField(max_length=120, blank=True, db_column='kk_kinnig_skoueriekaat', default="")
    proposal_author = models.TextField(db_column='kk_goulenner', blank=True, default="")
    square_bf = models.CharField(max_length=5, db_column='kk_karrezenn', blank=True, default="")
    longitude = models.DecimalField(max_digits=22, decimal_places=16, null=True, blank=True,
                                    db_column='kk_daveenn_douaroniel_lg')
    latitude = models.DecimalField(max_digits=22, decimal_places=16, null=True, blank=True,
                                   db_column='kk_daveenn_douaroniel_lt')
    etymological_note_bre = models.TextField(db_column='kk_gerdarzh_bre', blank=True, default="")
    etymological_note_fra = models.TextField(db_column='kk_gerdarzh_fra', blank=True, default="")
    created_at = models.DateTimeField(default=now, db_column='kk_deiziad_ebarzhin')
    created_by = models.ForeignKey('auth.User', null=True, related_name='locations', on_delete=models.SET_NULL,
                                   db_column='kk_aozer_ar_fichenn')
    is_name_of_day = models.BooleanField(default=False, db_column='kk_anv_deiz')
    old_id = models.IntegerField(null=True)


class StandardizedForm(models.Model):
    class Meta:
        db_table = 'kerofis_stumm_skouer'

    location = models.ForeignKey(Location, null=True, related_name='standardized_forms', on_delete=models.SET_NULL,
                                 db_column='kss_niv')
    standardized_form = models.CharField(max_length=100, db_column='kss_dibab')
    date = models.DateField(null=True, db_column='kss_deiziad_degemer')


class Informant(models.Model):
    class Meta:
        db_table = 'kerofis_titourer'

    first_name = models.CharField(max_length=100, default='', db_column='kt_anv_bihan_titourer')
    last_name = models.CharField(max_length=200, default='', db_column='kt_anv_titourer')
    surname = models.CharField(max_length=50, default='', db_column='kt_lesanv')
    occupation = models.CharField(max_length=200, default='', db_column='kt_micher')
    birthdate = models.CharField(max_length=4, default='', db_column='kt_bloaz_ganedigezh')
    birthplace = models.CharField(max_length=50, default='', db_column='kt_lech_ganedigezh')
    cities = models.CharField(max_length=250, default='', db_column='kt_kumun_titouret')
    arrival_date = models.CharField(max_length=4, default='', db_column='kt_pegoulz_er_gumun')
    notes = models.TextField(default='', db_column='kt_notenn')
    contact = models.TextField(default='', db_column='kt_darempred')
    interviewed_by = models.ForeignKey('auth.User', null=True, on_delete=models.SET_NULL, db_column='kt_enklasker')
    old_id = models.IntegerField(null=True)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def display(self):
        interviewed = f"{self.interviewed_by.first_name} {self.interviewed_by.last_name}" if self.interviewed_by else ""
        return f"{self.first_name} {self.last_name} ({self.pk} {interviewed})"


class PhoneticTranscription(models.Model):
    class Meta:
        db_table = 'kerofis_distagadur'

    location = models.ForeignKey(Location, null=True, related_name='phonetic_transcriptions', on_delete=models.SET_NULL,
                                 db_column='kd_niv')
    phonetic_transcription = models.CharField(max_length=255, db_column='kd_distagadur')
    is_standard = models.BooleanField(default=False, db_column='kd_distagadur_skouer')
    informant = models.ForeignKey(Informant, null=True, on_delete=models.SET_NULL, db_column='kd_titourer')
    created_at = models.CharField(max_length=10, null=True, db_column='kd_deziad')


class PhoneticTranscriptionLink(models.Model):
    class Meta:
        db_table = 'kerofis_distagadur_enrolladenn'

    phonetic_transcription = models.ForeignKey(PhoneticTranscription, null=True, related_name='links',
                                               on_delete=models.SET_NULL, db_column='kde_niv')
    link = models.FileField(db_column='kde_distagadur_enrolladenn')


class OldForm(models.Model):
    class Meta:
        db_table = 'kerofis_stumm_kozh'

    location = models.ForeignKey(Location, null=True, related_name='old_forms', on_delete=models.SET_NULL,
                                 db_column='ksk_niv')
    old_form = models.CharField(max_length=100, db_column='ksk_stumm')
    litteral_year = models.CharField(max_length=30, db_column='ksk_bloavezh')
    year = models.PositiveSmallIntegerField(null=True, db_column='ksk_bloavezh_niverel')
    book = models.ForeignKey('commun.Book', null=True, on_delete=models.SET_NULL, db_column='ksk_mammenn')
    reference = models.TextField(db_column='ksk_daveenn')


class AttestedForm(models.Model):
    class Meta:
        db_table = 'kerofis_stumm_testeniekaet'

    location = models.ForeignKey(Location, null=True, related_name='attested_forms', on_delete=models.SET_NULL,
                                 db_column='kst_niv')
    attested_form = models.CharField(max_length=80, null=True, db_column='kst_stumm')
    is_labeled = models.BooleanField(default=True, db_column='kst_stumm_skouer')
    litteral_year = models.CharField(max_length=10, db_column='kst_bloavezh')
    year = models.PositiveSmallIntegerField(null=True, db_column='kst_bloavezh_niverel')
    book = models.ForeignKey('commun.Book', null=True, on_delete=models.SET_NULL, db_column='kst_mammenn')
    reference = models.TextField(db_column='kst_daveenn')


class OtherForm(models.Model):
    class Meta:
        db_table = 'kerofis_stumm_all'

    location = models.ForeignKey(Location, null=True, related_name='other_forms', on_delete=models.SET_NULL,
                                 db_column='ksa_niv')
    usage_form = models.CharField(max_length=100, db_column='ksa_stumm')
    litteral_year = models.CharField(max_length=12, db_column='ksa_bloavezh')
    year = models.PositiveSmallIntegerField(null=True, db_column='ksa_bloavezh_niverel')
    book = models.ForeignKey('commun.Book', null=True, on_delete=models.SET_NULL, db_column='ksa_mammenn')
    reference = models.TextField(db_column='ksa_daveenn')


class TermSearchQuery(models.Model):
    class Meta:
        db_table = 'kerofis_enklaskou'

    query = models.CharField(max_length=200, null=None, db_column='ke_goulenn', unique=True)
    query_type = models.CharField(max_length=2, null=None, db_column='ke_oberataer')
    date = models.DateTimeField(db_column='ke_deiziad')
    counter = models.IntegerField(null=None, db_column='ke_konter_reket')
    results_number = models.IntegerField(null=None, db_column='ke_konter_disoch')
