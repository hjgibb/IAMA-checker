# Generated by Django 5.0.4 on 2024-05-20 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0021_law_phas4answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='law',
            name='status',
            field=models.CharField(choices=[('CP', 'complete'), ('ICP', 'incomplete'), ('CO', 'cut-off')], default='ICP', max_length=4),
        ),
    ]
