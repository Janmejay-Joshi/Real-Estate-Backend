# Generated by Django 4.0.2 on 2022-02-09 06:15

from django.db import migrations, models
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0007_alter_propertymodel_city_alter_propertymodel_state_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', versatileimagefield.fields.VersatileImageField(upload_to='images/', verbose_name='Image')),
                ('image_ppoi', versatileimagefield.fields.PPOIField(default='0.5x0.5', editable=False, max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='propertymodel',
            name='image',
            field=models.ManyToManyField(related_name='products', to='properties.Image'),
        ),
    ]
