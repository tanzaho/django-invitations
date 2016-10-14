# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import invitations.models


class Migration(migrations.Migration):

    dependencies = [
        ('invitations', '0005_auto_20160725_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='unsubscribe_slug',
            field=models.SlugField(default=invitations.models._create_unsubscribe_slug, max_length=32),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='invitation',
            name='want_mails',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
