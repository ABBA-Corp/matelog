# Generated by Django 4.1 on 2023-02-25 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0002_rename_youtube_staticinformation_linked_in_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventimages',
            name='event',
        ),
        migrations.DeleteModel(
            name='FAQ',
        ),
        migrations.RemoveField(
            model_name='imagegalleryfiles',
            name='gallery',
        ),
        migrations.RemoveField(
            model_name='videogalleryvideos',
            name='gallery',
        ),
        migrations.DeleteModel(
            name='EventImages',
        ),
        migrations.DeleteModel(
            name='Events',
        ),
        migrations.DeleteModel(
            name='ImageGalery',
        ),
        migrations.DeleteModel(
            name='ImageGalleryFiles',
        ),
        migrations.DeleteModel(
            name='VideoGalery',
        ),
        migrations.DeleteModel(
            name='VideoGalleryVideos',
        ),
    ]
