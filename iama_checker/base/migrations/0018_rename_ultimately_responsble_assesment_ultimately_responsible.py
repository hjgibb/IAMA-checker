# Generated by Django 4.2.7 on 2024-03-18 12:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_assesment_ultimately_responsble_assesment_user_group'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assesment',
            old_name='ultimately_responsble',
            new_name='ultimately_responsible',
        ),
    ]
