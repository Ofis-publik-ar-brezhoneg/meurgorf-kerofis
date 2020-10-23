# coding: utf8
from contextlib import suppress
import sys
import traceback

import mysql.connector
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from commun import models as commun_models
from meurgorf import models as meurgorf_models
from kerofis import models as kerofis_models

saved_instances = {}


def fix_accents(text):
    for i, j in (
            ('Ã©', 'é'),
            ('Ã¨', 'è'),
            ('Ã¯', 'ï'),
            ('Ã´', 'ô'),
            ('Ã§', 'ç'),
            ('Ãª', 'ê'),
            ('Ã¹', 'ù'),
            ('Ã¦', 'æ'),
            ('Å', 'œ'),
            ('Ã«', 'ë'),
            ('Ã¼', 'ü'),
            ('Ã±', 'ñ'),
            ('Â«', '«'),
            ('Â»', '»'),
            ('Ã¢', 'â'),
            ('Ã ', 'à'),

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


def get_location(current_row):
    try:
        return kerofis_models.Location.objects.get(old_id=current_row['niv'])
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


def get_city(current_row):
    try:
        return kerofis_models.City.objects.get(insee_code=current_row['insee'])
    except:
        print("city", current_row['insee'])


def get_department(current_row):
    try:
        return kerofis_models.Department.objects.get(current_row['dpt'])
    except:
        print("department", current_row['dpt'])


def get_department_from_code_postal(current_row):
    try:
        return kerofis_models.Department.objects.get(current_row['code_postal'][:2])
    except:
        print("department", current_row['code_postal'])


def get_category(current_row):
    if current_row['rummad'] == "":
        return None

    try:
        return kerofis_models.Category.objects.get(name_bre=current_row['rummad'])
    except Exception as e:
        print(current_row['rummad'])
        return None


def get_informant(current_row):
    try:
        return kerofis_models.Informant.objects.get(old_id=current_row['ntitourer'])
    except Exception as e:
        print(current_row['ntitourer'])
        return None


def get_user(attr):
    print(1)
    users = {}
    for user in User.objects.all():
        users[user.first_name + " " + user.last_name] = user

    def func(current_row):
        return users.get(current_row[attr])

    return func


def get_stumm(current_row):
    return fix_accents(current_row["stumm"].split('(')[0].strip())


def get_stumm_normalized(current_row):
    res = current_row["stumm"].split('(')
    if len(res) > 1:
        return fix_accents(res[1][:-1])
    return ""


tables = {
    "hollek_berradur": {
        "model": commun_models.Book,
        "fields": {
            'abbrevation': 'berradur',
            'title': 'levr',
            # 'description': ?
            'is_kerofis_old': 'kerofis_kozh',
            'is_kerofis_attested': 'kerofis_testeniekaet',
            'is_kerofis_other': 'kerofis_all',
            'is_meurgorf': 'meurgorf',
            'author': 'skrivagner',
            'is_active': 'bev',
        }
    },
    "meurgorf_pennger": {
        "model": meurgorf_models.Term,
        "fields": {
            'canonic_form': 'pennger',
            'grammatical_category': from_model(meurgorf_models.GrammaticalCategory, 'title_bre', 'rummenn_ger'),
            'can_be_edited': 'aotre_da_embann',
            'on_ndbf': 'ndbf',
            'on_gbahe': 'gbahe',
            'definition': 'termenadur',
            'study_notes': 'notennou_studian',
            'etymology': 'gerdarzh',
            'old_id': 'niv'
            # 'parents':
            # 'usage':
        }
    },
    "meurgorf_adstummou": {
        "model": meurgorf_models.Variant,
        "fields": {
            "term": get_term,
            "variant": "adstumm"
        }
    },
    "meurgorf_stummou_deveret": {
        "model": meurgorf_models.DerivedForm,
        "fields": {
            "term": get_term,
            "order": "urzh",
            "sub_order": "isurzh",
            "form": "stumm"
        }
    },
    "meurgorf_stummou_istorel": {
        "model": meurgorf_models.HistoricalOccurrence,
        "fields": {
            "occurence": get_stumm,
            "occurence_normalized": get_stumm_normalized,
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
            "term": get_term,
            "reference": related_object("meurgorf_stummou_istorel", "id")
        },
    },
    "administration_utilisateur": {
        "model": User,
        "fields": {
            "username": "administration_utilisateur_login",
            "first_name": "administration_utilisateur_prenom",
            "last_name": "administration_utilisateur_nom",
            "is_active": "administration_utilisateur_actif",
            "date_joined": "administration_utilisateur_dateinsertion"
       }
    },
    "toponymie_lechanvadurezh l inner join toponymie_stummou_testeniekaet t on l.niv = t.niv where rummad = 'Departamant' group by l.niv": {
        "model": kerofis_models.Department,
        "fields": {
            "code": "dpt",
            "name_fra": "lec_hanv",
            "name_bre": "stumm"
        }
    },
    "toponymie_kumuniou_breizh": {
        "model": kerofis_models.City,
        "fields": {
            "insee_code": "code_insee",
            "postal_code": "code_postal",
            "department": get_department_from_code_postal,
            "name_bre": "kumun",
            "name_fra": "commune"
        }
    },
    "toponymie_rummad": {
        "model": kerofis_models.Category,
        "fields": {
            "name_bre": "rummad",
            "name_fra": "categorie"
        }
    },
    "toponymie_lechanvadurezh": {
        "model": kerofis_models.Location,
        "fields": {
            "name": "lec_hanv",
            "on_ign": "kaset_da_ign",
            # "ign_date": ??,
            "formalized_date": "deiziad",
            "is_public": "aotre_da_embann",
            "generic_name": "stagadenn",
            "on_bf": "kartenn_blay_foldex",
            "city": get_city,
            "department": get_department,
            "category": get_category,
            "reference": "daveennou",
            "notes": "notennou_studian",
            "formalized_proposal": "kinnig_skoueriakaet",
            "proposal_author": "goulenner",
            "created_at": "deiziad_ebarzhin",
            "created_by": get_user("saver_ar_fichenn"),
            "square_bf": "karrezenn",
            # "longitude": get_longitude "ledred"
            # "latitude": get_latitude "ledred"
            "etymological_note_bre": "gerdarzh_bzh",
            "etymological_note_fra": "gerdarzh_galleg",
            "old_id": "niv"
        }
    },
    "toponymie_sk": {
        "model": kerofis_models.StandardizedForm,
        "fields": {
            "standardized_form": "dibab",
            "date": "deiziad_degemer",
            "location": get_location
        }
    },
    "toponymie_titourer": {
        "model": kerofis_models.Informant,
        "fields": {
            "first_name": "anv_bihan_titourer",
            "last_name": "anv_titourer",
            "surname": "lesanv",
            "occupation": "micher",
            "birthdate": "bloavezh_ganedigezh",
            "birthplace": "lech_ganedigezh",
            # "cities": "",
            "arrival_date": "abaoe_pegoulz_er_gumun",
            "notes": "notennou",
            "contact": "darempred",
            "interviewed_by": get_user("anv_enklasker"),
            "old_id": "ntitourer"
        }
    },
    "toponymie_distagaduriou": {
        "model": kerofis_models.PhoneticTranscription,
        "fields": {
            "location": get_location,
            "phonetic_transcription": "distagadur",
            "informant": get_informant,
            "created_at": "deiziad"
        }
    },
    "toponymie_stummou_kozh": {
        "model": kerofis_models.OldForm,
        "fields": {
            "location": get_location,
            "old_form": "stumm",
            "litteral_year": "bloavezh",
            "year": "bloavezh_int",
            "book": get_book,
            "reference": "daveenn"
        }
    },
    "toponymie_stummou_testeniekaet": {
        "model": kerofis_models.AttestedForm,
        "fields": {
            "location": get_location,
            "attested_form": "stumm",
            "litteral_year": "bloavezh",
            "book": get_book,
            "reference": "daveenn"
        }
    },
    "toponymie_stummou_all": {
        "model": kerofis_models.OtherForm,
        "fields": {
            "location": get_location,
            "usage_form": "stumm",
            "litteral_year": "bloavezh",
            "book": get_book,
            "reference": "daveenn"
        }
    }
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
                print(row)
                traceback.print_exc(file=sys.stdout)

        conn.close()
