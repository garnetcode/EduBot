# Generated by Django 3.2.12 on 2023-02-13 07:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_course_duration'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('packages', '0010_alter_package_service_type'),
        ('subscriptions', '0004_auto_20230212_1139'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscription',
            old_name='expires_at',
            new_name='expiry_date',
        ),
        migrations.AlterField(
            model_name='subscription',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_subscription', to='courses.course'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='package',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='package_subscription', to='packages.package'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_subscription', to=settings.AUTH_USER_MODEL),
        ),
    ]
