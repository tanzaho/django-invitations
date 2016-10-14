# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invitations', '0005_auto_20160725_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='unsubscribe_slug',
            field=models.SlugField(max_length=32, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='invitation',
            name='want_mails',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
