from django.db.models.fields.reverse_related import ManyToOneRel
from django.db.models.fields.reverse_related import ManyToManyRel
from django.db.models.fields.related import ManyToManyField
from django.db.models.fields.related import ForeignKey

from django.contrib.auth.models import User


def get_all_fields_info(model_class, prefix="", ignore_relations=[]):
    fields = {}
    related_prefix = f"{prefix}__" if prefix else ""

    if model_class == User:
        return {f"{prefix}_username": f"{related_prefix}username"}

    for field in model_class._meta.get_fields():
        if field.name == 'id':
            continue  # skip id field
        if isinstance(field, (ManyToOneRel, ManyToManyRel)):
            if field.related_model not in ignore_relations:
                fields.update(get_all_fields_info(
                    field.related_model,
                    f"{related_prefix}{field.related_name}",
                    [*ignore_relations, model_class]
                ))
        elif isinstance(field, ManyToManyField):
            continue  # ignore many to many for now
        elif isinstance(field, ForeignKey):
            if field.related_model not in ignore_relations:
                fields.update(get_all_fields_info(
                    field.related_model,
                    f"{related_prefix}{field.name}",
                    [*ignore_relations, model_class]
                ))
        else:
            field_info = field.get_attname_column()
            fields.update({field_info[1]: f"{related_prefix}{field_info[0]}"})

    return fields
