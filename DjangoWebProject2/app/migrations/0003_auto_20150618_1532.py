# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20150618_1531'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mensaje',
            old_name='asd',
            new_name='usuario',
        ),
        migrations.RenameField(
            model_name='reporte',
            old_name='Administrador',
            new_name='administrador',
        ),
    ]
