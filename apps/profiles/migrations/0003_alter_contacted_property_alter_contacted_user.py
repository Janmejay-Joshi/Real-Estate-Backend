# Generated by Django 4.0.2 on 2022-02-19 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0002_alter_propertymodel_bathrooms_and_more'),
        ('profiles', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacted',
            name='property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contacted_property', to='properties.propertymodel'),
        ),
        migrations.AlterField(
            model_name='contacted',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contact_profile', to='profiles.userprofilemodel'),
        ),
    ]
