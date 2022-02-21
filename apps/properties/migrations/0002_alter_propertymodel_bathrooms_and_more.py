# Generated by Django 4.0.2 on 2022-02-19 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertymodel',
            name='bathrooms',
            field=models.CharField(blank=True, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4+', '4+')], max_length=2),
        ),
        migrations.AlterField(
            model_name='propertymodel',
            name='bedrooms',
            field=models.CharField(blank=True, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5+', '5+')], max_length=2),
        ),
        migrations.AlterField(
            model_name='propertymodel',
            name='floor',
            field=models.CharField(choices=[('Basement', 'Basement'), ('Ground', 'Ground'), ('1-4', '1-4'), ('5-8', '5-8'), ('9-12', '9-12'), ('13+', '13+')], max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='propertymodel',
            name='for_status',
            field=models.CharField(blank=True, choices=[('sale', 'Sale'), ('rent', 'Rent'), ('pg', 'Paying Geust')], max_length=4),
        ),
        migrations.AlterField(
            model_name='propertymodel',
            name='furnishing_status',
            field=models.CharField(blank=True, choices=[('furnished', 'Furnished'), ('semifurnished', 'Semi furnished'), ('unfurnished', 'Unfurnished')], max_length=25),
        ),
        migrations.AlterField(
            model_name='propertymodel',
            name='possession',
            field=models.CharField(blank=True, choices=[('under construction', 'Under Construction'), ('ready to move', 'Ready To Move')], max_length=25),
        ),
    ]