from django.db import models


class Book(models.Model):
    class Meta:
        db_table = 'hollek_mammenn'
        verbose_name = 'Oberenn'
        ordering = ['abbrevation']

    abbrevation = models.CharField(max_length=15, unique=True, null=False, db_column='hm_mammenn_berradur')
    title = models.TextField(null=False, blank=False, db_column='hm_mammenn_levr')
    description = models.TextField(null=False, blank=True, db_column='hm_mammenn_deskrivadur')
    is_kerofis_old = models.BooleanField(db_column='hm_mammenn_kozh', default=False)
    is_kerofis_other = models.BooleanField(db_column='hm_mammenn_all', default=False)
    is_kerofis_attested = models.BooleanField(db_column='hm_mammenn_testeniekaet', default=False)
    is_meurgorf = models.BooleanField(db_column='hm_mammenn_meurgorf', default=False)
    author = models.CharField(max_length=100, db_column='hm_mammenn_aozer', blank=True, default='')
    is_active = models.BooleanField(default=True, db_column='hm_mammenn_bev')
