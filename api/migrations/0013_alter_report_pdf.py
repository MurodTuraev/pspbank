# Generated by Django 3.2.4 on 2021-07-19 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20210719_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='pdf',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
