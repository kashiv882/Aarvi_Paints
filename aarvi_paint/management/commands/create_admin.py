from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create or delete superuser'

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete',
            action='store_true',
            help='Delete the admin user',
        )

    def handle(self, *args, **options):
        User = get_user_model()
        username = 'aarvi'
        email = 'admin@example.com'
        password = 'aarvi'

        if options['delete']:
            # Delete admin user if exists
            if User.objects.filter(username=username).exists():
                User.objects.filter(username=username).delete()
                self.stdout.write(self.style.SUCCESS(f'Admin user "{username}" deleted'))
            else:
                self.stdout.write(self.style.WARNING(f'Admin user "{username}" does not exist'))
        else:
            # Create admin user if not exists
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(username, email, password)
                self.stdout.write(self.style.SUCCESS(f'Admin user "{username}" created'))
                self.stdout.write(f'Username: {username}')
                self.stdout.write(f'Email: {email}')
                self.stdout.write(f'Password: {password}')  # Only for dev/testing
            else:
                self.stdout.write(self.style.WARNING(f'Admin user "{username}" already exists'))
