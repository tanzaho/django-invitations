# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import invitations.models
from invitations.models import Invitation, _create_unsubscribe_slug


class Migration(migrations.Migration):

    dependencies = [
        ('invitations', '0005_auto_20160725_1814'),
    ]

    def set_unsub_slug(apps, schema_editor):
        for row in Invitation.objects.all():
            row.unsubscribe_slug = _create_unsubscribe_slug()
            row.save()

    operations = [

        migrations.AddField(
            model_name='invitation',
            name='unsubscribe_slug',
            field=models.SlugField(default=invitations.models._create_unsubscribe_slug, max_length=32),
            preserve_default=True,
        ),

        migrations.RunPython(set_unsub_slug),

        migrations.AlterField(
            model_name='invitation',
            name='unsubscribe_slug',
            field=models.SlugField(default=invitations.models._create_unsubscribe_slug, unique=True, max_length=32),
        ),
    ]
