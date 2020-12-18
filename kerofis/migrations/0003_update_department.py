from django.db import migrations, models


def update_department(apps, schema_editor):
    Department = apps.get_model("kerofis", "Department")
    City = apps.get_model("kerofis", "City")
    departments = {}
    for department in Department.objects.all():
        departments[department.code] = department

    for city in City.objects.all():
        if len(str(city.postal_code)) > 4:
            department = departments.get(str(city.postal_code)[:2])
            city.department = department
            city.save()
            for location in city.locations.all():
                location.department = department
                location.save()


class Migration(migrations.Migration):

    dependencies = [
        ('kerofis', '0002_auto_20201218_1540'),
    ]

    operations = [
        migrations.RunPython(update_department, migrations.RunPython.noop),
    ]
