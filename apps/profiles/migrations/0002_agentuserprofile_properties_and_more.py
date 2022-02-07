# Generated by Django 4.0.2 on 2022-02-07 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0001_initial'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='agentuserprofile',
            name='properties',
            field=models.ManyToManyField(related_name='agent_properties', to='properties.PropertyModel'),
        ),
        migrations.AddField(
            model_name='agentuserprofile',
            name='wishlist',
            field=models.ManyToManyField(related_name='agent_whitelist', to='properties.PropertyModel'),
        ),
        migrations.AddField(
            model_name='buyeruserprofile',
            name='wishlist',
            field=models.ManyToManyField(related_name='buyer_wishlist', to='properties.PropertyModel'),
        ),
        migrations.AddField(
            model_name='selleruserprofile',
            name='properties',
            field=models.ManyToManyField(related_name='user_properties', to='properties.PropertyModel'),
        ),
    ]
