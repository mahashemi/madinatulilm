from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0003_testimonial'),
    ]

    operations = [
        # Remove the old single image field from Announcement
        migrations.RemoveField(
            model_name='announcement',
            name='image',
        ),
        # Remove youtube_url and video_embed_code (they are already in the DB from 0002;
        # we keep them — nothing to do — but we must NOT re-add them. They stay.)
        # Create the new AnnouncementImage table
        migrations.CreateModel(
            name='AnnouncementImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='announcements/images/')),
                ('caption', models.CharField(blank=True, help_text='Short caption shown below this image', max_length=300)),
                ('sort_order', models.PositiveSmallIntegerField(default=0, help_text='Lower number = shown first')),
                ('announcement', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='images',
                    to='announcements.announcement',
                )),
            ],
            options={
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
                'ordering': ['sort_order', 'id'],
            },
        ),
    ]
