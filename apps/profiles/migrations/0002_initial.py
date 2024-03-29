# Generated by Django 4.0.2 on 2022-02-18 08:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0001_initial'),
        ('properties', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofilemodel',
            name='image',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cover', to='properties.image'),
        ),
        migrations.AddField(
            model_name='userprofilemodel',
            name='prime_status',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile_prime', to='profiles.primemodel'),
        ),
        migrations.AddField(
            model_name='userprofilemodel',
            name='properties',
            field=models.ManyToManyField(blank=True, related_name='properties', to='properties.PropertyModel'),
        ),
        migrations.AddField(
            model_name='userprofilemodel',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userprofilemodel',
            name='wishlist',
            field=models.ManyToManyField(blank=True, related_name='wishlist', to='properties.PropertyModel'),
        ),
        migrations.AddField(
            model_name='contacted',
            name='property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='contacted_property', to='properties.propertymodel'),
        ),
        migrations.AddField(
            model_name='contacted',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='contact_profile', to='profiles.userprofilemodel'),
        ),
    ]
