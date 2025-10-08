# myapp/management/commands/startup.py
from django.core.management.base import BaseCommand
import random
import string
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "generate users"
    def add_arguments(self, parser):
        # Positional argument (required)
        parser.add_argument('task', nargs='?', default='default', help='Name of the startup task to run')

        # Optional flag (e.g., --force)
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force execution even if already initialized'
        )

        # Optional argument with a value (e.g., --count 3)
        parser.add_argument(
            '--count',
            type=int,
            default=1,
            help='Number of times to repeat the task'
        )

    def handle(self, *args, **options):
        task = options['task']
        force = options['force']
        count = options['count']
        
        create_random_users(count)
        self.stdout.write(self.style.NOTICE(f"Running task '{task}' (force={force}, count={count})"))





def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_random_users(n=100):
    for i in range(n):
        username = f"user_{generate_random_string(6)}"
        password = generate_random_string(10)
        first_name = generate_random_string(8)
        last_name = generate_random_string(10)
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            print(f"✅ Created: {username} / {password} / {first_name} {last_name}")
        else:
            print(f"❌ Skipped (already exists): {username}")