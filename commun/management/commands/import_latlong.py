# coding: utf8
from contextlib import suppress
import sys
import traceback

import mysql.connector
from django.core.management.base import BaseCommand

from kerofis.models import Location

saved_instances = {}


class Command(BaseCommand):
    help = 'Import the lat lng'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        conn = mysql.connector.connect(host="localhost", user="root", password="root", database="leslicgm_i4gj", use_unicode=True, charset='utf8')
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SET NAMES utf8mb4;")  # or utf8 or any other charset you want to handle
        cursor.execute("SET CHARACTER SET utf8mb4;")  # same as above
        cursor.execute("SET character_set_connection=utf8mb4;")  # same as above

        cursor.execute(f"select * from villes_france_free where ville_departement not in ('2A', '2B');")
        for row in cursor.fetchall():
            Location.objects.filter(city__insee_code=row['ville_code_commune'], category__in=[1, 19, 20, 21]).update(
                latitude=row['ville_latitude_deg'], longitude=row['ville_longitude_deg'])

        conn.close()
