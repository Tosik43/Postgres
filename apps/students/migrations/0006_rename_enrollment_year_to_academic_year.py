from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("students", "0005_changereason_educationhistory"),
    ]

    operations = [
        migrations.RenameField(
            model_name="educationhistory",
            old_name="enrollment_year",
            new_name="academic_year",
        ),
    ]