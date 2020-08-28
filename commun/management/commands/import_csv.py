# coding: utf8
import csv

from django.core.management.base import BaseCommand, CommandError

from commun import models as commun_models
from meurgorf import models as meurgorf_models


class Command(BaseCommand):
    help = 'Import the csv'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)
        parser.add_argument('--rummenn', action='store_true')
        parser.add_argument('--kerofis', action='store_true')

    def handle(self, *args, **options):
        with open(options['file']) as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader[1:]:
                if options['rummenn']:
                    obj = meurgorf_models.GrammaticalCategory()
                    obj.title_bre = row[0]
                    obj.title_fra = row[1]
                    obj.save()
