"""Peewee migrations -- 003_common.py.

Some examples (model - class or model name)::

    > Model = migrator.orm['model_name']            # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.python(func, *args, **kwargs)        # Run python code
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.drop_index(model, *col_names)
    > migrator.add_not_null(model, *field_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)

"""

import datetime as dt
import peewee as pw


def migrate(migrator, database, fake=False, **kwargs):
    """Write your migrations here."""
    migrator.add_fields('user', pending_action=pw.IntegerField(default=0))
    migrator.change_fields('user',
                           telegram_login=pw.TextField(default=''),
                           is_moderator=pw.BooleanField(default=False),
                           is_active=pw.BooleanField(default=True))
    migrator.add_not_null('user', 'telegram_login')


def rollback(migrator, database, fake=False, **kwargs):
    """Write your rollback migrations here."""
    migrator.remove_fields('user', 'pending_action')
    migrator.drop_not_null('user', 'telegram_login')
