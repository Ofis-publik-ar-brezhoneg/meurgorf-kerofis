from django.db import models
from django.utils.timezone import now


class Usage:
    VERY_USUAL = '3'
    USUAL = '2'
    UNCOMMON = '1'


class GrammaticalCategory(models.Model):
    class Meta:
        db_table = 'meurgorf_rummen_ger'

    title_bre = models.CharField(max_length=40, db_column='mrg_rummenn_ger_bre')
    title_fra = models.CharField(max_length=40, db_column='mrg_rummenn_ger_fra')
    abbreviation_bre = models.CharField(max_length=5, db_column='mrg_rummenn_ger_berradur_bre')
    abbreviation_fra = models.CharField(max_length=5, db_column='mrg_rummenn_ger_berradur_fra')


class Term(models.Model):
    class Meta:
        db_table = 'meurgorf_pennger'

    canonic_form = models.TextField(null=False, blank=False, db_column='mp_pennger')
    grammatical_category = models.ForeignKey(GrammaticalCategory, related_name='terms', on_delete=models.CASCADE,
                                             db_column='mp_rummenn_ger')
    can_be_edited = models.BooleanField(db_column='mp_aotre_embann', default=True)
    on_ndbf = models.BooleanField(db_column='mp_ndbf', default=False)
    on_gbahe = models.BooleanField(db_column='mp_gbahe', default=False)
    definition = models.TextField(db_column='mp_termenadur', blank=True, default='')
    study_notes = models.TextField(db_column='mp_noteen_studi', blank=True, default='')
    etymology = models.TextField(db_column='mp_gerdarzh', blank=True, default='')
    parents = models.ManyToManyField('self', db_table='meurgorf_pennger_kar')
    created_at = models.DateTimeField(default=now, db_column='mp_deziad_foran')
    created_by = models.ForeignKey('auth.User', null=True, related_name='terms', on_delete=models.SET_NULL,
                                   db_column='mp_aozer')
    updated_at = models.DateTimeField(null=True)
    updated_by = models.ForeignKey('auth.User', null=True, related_name='+', on_delete=models.SET_NULL)
    usage = models.SmallIntegerField(default=Usage.USUAL, choices=[
        (Usage.VERY_USUAL, 'Very Usual'),
        (Usage.USUAL, 'Usual'),
        (Usage.UNCOMMON, 'uncommon')
    ], db_column='mp_implij')
    old_id = models.IntegerField(null=True)

    @property
    def usage_label_fra(self):
        return {
            1: 'Peu courant',
            2: 'Courant',
            3: 'Très courant'
        }[self.usage]

    @property
    def usage_label_bre(self):
        return {
            1: 'Rouez',
            2: 'Stank',
            3: 'Pemdez'
        }[self.usage]


class Variant(models.Model):
    class Meta:
        db_table = 'meurgorf_adpennger'

    term = models.ForeignKey(Term, related_name='variants', null=True, on_delete=models.SET_NULL, db_column='ma_niv')
    variant = models.CharField(max_length=50, db_column='ma_adpennger')


class DerivedForm(models.Model):
    class Meta:
        db_table = 'meurgorf_furm_deveret'
        ordering = ['order', 'sub_order']

    term = models.ForeignKey(Term, related_name='derived_forms', null=True, on_delete=models.SET_NULL,
                             db_column='mfd_niv')
    order = models.PositiveSmallIntegerField(db_column='mfd_urzh')
    sub_order = models.PositiveSmallIntegerField(default=0, db_column='mfd_isurzh')
    form = models.TextField(db_column='mfd_stumm')


class HistoricalOccurrenceOccurrence(models.Model):
    class Meta:
        db_table = 'meurgorf_degouezh'

    reference = models.ForeignKey('HistoricalOccurrence', null=True, on_delete=models.SET_NULL,
                                  db_column='md_id_skouer_istorel')
    term = models.ForeignKey(Term, db_column='md_niv_pennger', null=True, on_delete=models.SET_NULL,)


class HistoricalOccurrence(models.Model):
    class Meta:
        db_table = 'meurgorf_skouer_istorel'
        ordering = ['year']

    occurence = models.TextField(db_column='msi_skouer')
    occurence_normalized = models.TextField(db_column='msi_skouer_peurunvan', blank=True, default='')
    litteral_year = models.CharField(max_length=10, db_column='msi_bloavezh')
    year = models.PositiveSmallIntegerField(db_column='msi_bloavezh_niverel')
    book = models.ForeignKey('commun.Book', null=True, on_delete=models.SET_NULL, db_column='msi_mammenn')
    reference = models.TextField(db_column='msi_daveenn')
    terms = models.ManyToManyField(Term, related_name="historical_occurrences", through=HistoricalOccurrenceOccurrence)


class PhoneticForm(models.Model):
    class Meta:
        db_table = 'meurgorf_distagadur'

    term = models.ForeignKey(Term, related_name='phonetic_forms', null=True, on_delete=models.SET_NULL,
                             db_column='md_niv')
    phonetic_form = models.TextField(null=True, db_column='md_distagadur')
    phonetic_url = models.CharField(max_length=30, null=True, db_column='md_distagadur_enrolladenn')


class TermSearchQuery(models.Model):
    class Meta:
        db_table = 'meurgorf_enklaskou'

    query = models.CharField(max_length=200, null=None, db_column='me_reket', unique=True)
    query_type = models.CharField(max_length=2, null=None, db_column='me_oberataer')
    date = models.DateTimeField(db_column='me_deiziad')
    counter = models.IntegerField(null=None, db_column='me_konter_goulenn')
    results_number = models.IntegerField(null=None, db_column='me_konter_disoch')
