# Generated by Django 4.2.7 on 2024-01-31 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_assesment_date_last_saved'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_warning',
            field=models.CharField(default=None, max_length=140, null=True),
        ),
    ]
