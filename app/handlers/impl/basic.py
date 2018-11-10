from app.core.info import PROJECT_FULL_NAME
from app.handlers.context import Context
from app.models.all import User


def _maybe_greet_user(context: Context, user: User):
    if context.group not in user.groups:
        user.groups.append(context.group)
        message_template = _('greet_known_{user}') if user.is_known else _('greet_new_{user}')
        user.is_known = True
        context.send_response_message(message_template.format(user.name))


def _maybe_farewell_user(context: Context, user: User):
    if context.group in user.groups:
        user.groups.remove(context.group)
        context.send_response_message(_('farewell_{user}').format(user.name))


def process_users_and_groups(context: Context):
    # TODO: Should bot provide some help when it joins group?
    if not context.group:
        return
    if context.users_joined:
        for user in context.users_joined:
            _maybe_greet_user(context, user)
    if context.user_left:
        _maybe_farewell_user(context, context.user_left)


def on_help_or_start(context: Context):
    message_template = _('{project}_help_for_group') if context.group else _('{project}_help_for_private')
    context.send_response_message(message_template.format(project=PROJECT_FULL_NAME))