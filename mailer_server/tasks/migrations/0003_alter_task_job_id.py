# Generated by Django 3.2.4 on 2021-08-03 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20210803_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='job_id',
            field=models.CharField(blank=True, db_index=True, max_length=128, null=True),
        ),
    ]