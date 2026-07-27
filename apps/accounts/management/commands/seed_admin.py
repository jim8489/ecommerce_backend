from django.core.management.base import BaseCommand

from apps.accounts.models import User


class Command(BaseCommand):
    help = "Create default admin user"

    def handle(self, *args, **options):

        if User.objects.filter(email="admin@example.com").exists():
            self.stdout.write(
                self.style.WARNING(
                    "Admin already exists."
                )
            )
            return

        User.objects.create_superuser(
            email="admin@example.com",
            password="Admin123!",
            first_name="System",
            last_name="Administrator",
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Admin user created successfully."
            )
        )