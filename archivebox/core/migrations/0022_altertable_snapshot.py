from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_auto_20221109_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snapshot',
            name='url',
            field=models.URLField(db_index=True, unique=True, max_length=2200),
        ),
        migrations.AlterField(
            model_name='snapshot',
            name='title',
            field=models.CharField(blank=True, db_index=True, max_length=1024, null=True),
        ),
    ]
