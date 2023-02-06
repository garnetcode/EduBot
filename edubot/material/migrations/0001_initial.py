# Generated by Django 3.2.12 on 2023-02-04 05:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0003_course_duration'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('content_type', models.CharField(choices=[('video', 'Video'), ('audio', 'Audio'), ('document', 'Document'), ('image', 'Image'), ('other', 'Other')], max_length=255)),
                ('content', models.FileField(upload_to='materials/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='courses.course')),
            ],
        ),
    ]