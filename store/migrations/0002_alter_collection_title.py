# Generated by Django 4.0.5 on 2022-07-05 14:08

from django.db import migrations, models
import store.Validators


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='title',
            field=models.CharField(max_length=255, validators=[store.Validators.Title_validator]),
        ),
    ]