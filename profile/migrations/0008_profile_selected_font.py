# Generated by Django 4.2.4 on 2023-10-11 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0007_font_delete_userfontchoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='selected_font',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profile.font'),
        ),
    ]
