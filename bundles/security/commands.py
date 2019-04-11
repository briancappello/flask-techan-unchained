from flask_unchained import click, unchained
from flask_unchained.bundles.security import Security, SecurityService, UserManager
from flask_unchained.bundles.security.commands import users


security: Security = unchained.get_local_proxy('security')
security_service: SecurityService = unchained.get_local_proxy('security_service')
user_manager: UserManager = unchained.get_local_proxy('user_manager')


@users.command('create')
@click.option('--first-name', prompt='First name',
              help='The user\'s first name.')
@click.option('--last-name', prompt='Last name',
              help='The user\'s last name.')
@click.option('--username', prompt='Username',
              help="The username.")
@click.option('--email', prompt='Email address',
              help="The user's email address.")
@click.option('--password', prompt='Password',
              help='The user\'s password.',
              hide_input=True, confirmation_prompt=True)
@click.option('--active/--inactive', prompt='Should user be active?',
              help='Whether or not the new user should be active.',
              default=False, show_default=True)
@click.option('--confirmed-at', prompt='Confirmed at timestamp (or enter "now")',
              help='The date stamp the user was confirmed at (or enter "now") '
                   ' [default: None]',
              default=None, show_default=True)
@click.option('--send-email/--no-email', default=False, show_default=True,
              help='Whether or not to send the user a welcome email.')
def create_user(email, password, active, confirmed_at, send_email):
    """
    Create a new user.
    """
    if confirmed_at == 'now':
        confirmed_at = security.datetime_factory()
    user = user_manager.create(email=email, password=password, active=active,
                               confirmed_at=confirmed_at)
    if click.confirm(f'Are you sure you want to create {user!r}?'):
        security_service.register_user(user, allow_login=False, send_email=send_email)
        user_manager.save(user, commit=True)
        click.echo(f'Successfully created {user!r}')
    else:
        click.echo('Cancelled.')
