# coding: utf8
from contextlib import suppress
import sys
import traceback

import mysql.connector
from django.core.management.base import BaseCommand, CommandError

from commun import models as commun_models
from meurgorf import models as meurgorf_models


saved_instances = {}


def fix_accents(text):
    for i, j in (
            ('Ã±', 'ñ'),
            ('Ã¹', 'ù'),
            ('Ã©', 'é'),
            ('Ã¨', 'è'),
            ('Ã´', 'ô'),
            ('Â«', '«'),
            ('Â»', '»'),
            ('Ã§', 'ç'),

    ):
        text = text.replace(i, j)
    return text


class FakeOccurrence:
    niv = None
    istorel = None

    def save(self):
        pass


def related_object(table, current_row_id):
    def func(current_row):
        try:
            return saved_instances[table][current_row[current_row_id]]
        except Exception as e:
            if table == 'hollek_berradur':
                new_book = commun_models.Book(abbrevation=current_row[current_row_id])
                new_book.save()
                return new_book

            return None

    return func


def from_model(model, attr, current_row_id):
    def func(current_row):
        try:
            return model.objects.get(**{attr: fix_accents(current_row[current_row_id])})
        except Exception as e:
            print(e)
            print(attr, current_row[current_row_id])
            exit(-1)

    return func


def get_term(current_row):
    try:
        return meurgorf_models.Term.objects.get(old_id=current_row['niv'])
    except Exception as e:
        print(current_row['niv'])
        return None


def get_book(current_row):
    try:
        obj, created = commun_models.Book.objects.get_or_create(abbrevation=current_row['berradur'])
        if created:
            print('new', current_row['berradur'])
        return obj
    except Exception as e:
        print(e)
        print(current_row['berradur'])
        return None


tables = {
    # "hollek_berradur": {
    #     "model": commun_models.Book,
    #     "fields": {
    #         'abbrevation': 'berradur',
    #         'title': 'levr',
    #         # 'description': ?
    #         'is_kerofis_old': 'kerofis_kozh',
    #         'is_kerofis_attested': 'kerofis_testeniekaet',
    #         'is_kerofis_other': 'kerofis_all',
    #         'is_meurgorf': 'meurgorf',
    #         'author': 'skrivagner',
    #         'is_active': 'bev',
    #     },
    #     "id": "berradur"
    # },
    # "meurgorf_pennger": {
    #     "model": meurgorf_models.Term,
    #     "fields": {
    #         'canonic_form': 'pennger',
    #         'grammatical_category': from_model(meurgorf_models.GrammaticalCategory, 'title_bre', 'rummenn_ger'),
    #         'can_be_edited': 'aotre_da_embann',
    #         'on_ndbf': 'ndbf',
    #         'on_gbahe': 'gbahe',
    #         'definition': 'termenadur',
    #         'study_notes': 'notennou_studian',
    #         'etymology': 'gerdarzh',
    #         'old_id': 'niv'
    #         # 'parents':
    #         # 'usage':
    #     },
    #     "id": "niv"
    # },
    # "meurgorf_adstummou": {
    #     "model": meurgorf_models.Variant,
    #     "fields": {
    #         "term": related_object("meurgorf_pennger", "niv"),
    #         "variant": "adstumm"
    #     }
    # },
    # "meurgorf_stummou_deveret": {
    #     "model": meurgorf_models.DerivedForm,
    #     "fields": {
    #         "term": related_object("meurgorf_pennger", "niv"),
    #         "order": "urzh",
    #         "sub_order": "isurzh",
    #         "form": "stumm"
    #     }
    # },
    "meurgorf_stummou_istorel": {
        "model": meurgorf_models.HistoricalOccurrence,
        "fields": {
            "occurence": "stumm",
            # "occurence_normalized": "",
            "litteral_year": "bloavezh",
            "year": "bloavezh_int",
            "book": get_book,
            "reference": "daveenn",
        },
        "id": "id"
    },
    "meurgorf_stummou_istorel_degouezhiou": {
        "model": meurgorf_models.HistoricalOccurrenceOccurrence,
        "fields": {
            "term": get_term,  # related_object("meurgorf_pennger", "niv"),
            "reference": related_object("meurgorf_stummou_istorel", "id")
        },
    },
}


class Command(BaseCommand):
    help = 'Import the old database'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        conn = mysql.connector.connect(host="localhost", user="root", password="root", database="leslicgm_i4gj", use_unicode=True, charset='utf8')
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SET NAMES utf8mb4;")  # or utf8 or any other charset you want to handle
        cursor.execute("SET CHARACTER SET utf8mb4;")  # same as above
        cursor.execute("SET character_set_connection=utf8mb4;")  # same as above

        for table, info in tables.items():
            print(table)
            cursor.execute(f"select * from {table};")
            saved_instances[table] = {}
            childs = {}

            try:
                with suppress(Exception):
                    info['model'].objects.all().delete()

                for row in cursor.fetchall():
                    obj = info['model']()
                    for field_name, row_name in info['fields'].items():
                        if callable(row_name):
                            new_value = row_name(row)
                            if isinstance(new_value, list):
                                if field_name not in childs.keys():
                                    childs[field_name] = []
                                childs[field_name].extend(new_value)
                            else:
                                setattr(obj, field_name, new_value)
                        else:
                            new_value = row.get(row_name)
                            if isinstance(new_value, str):
                                new_value = fix_accents(new_value)
                            setattr(obj, field_name, new_value)
                    obj.save()

                    if childs:
                        print(childs)

                    for field_name, child_objs in childs.items():
                        getattr(obj, field_name).add(*child_objs)

                    if 'id' in info.keys():
                        saved_instances[table][row[info['id']]] = obj
                    if 'array' in info.keys():
                        if row[info['array']] not in saved_instances[table].keys():
                            saved_instances[table][row[info['array']]] = []
                        saved_instances[table][row[info['array']]].append(obj.niv)
            except Exception:
                traceback.print_exc(file=sys.stdout)

        conn.close()
