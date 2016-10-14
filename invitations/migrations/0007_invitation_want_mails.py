# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invitations', '0006_invitation_unsubscribe_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='want_mails',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
