from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand


class Command(BaseCommand):
    """Automate the creation of essential data.

    This command will be run during each deployment.
    """

    def handle(self, *args, **options):
        admin_user, created = get_user_model().objects.update_or_create(
            username="admin",
            defaults={
                "is_superuser": True,
                "is_staff": True,
                "is_active": True,
            }
        )
        if created:
            admin_user.set_password(settings.ADMIN_INITIAL_PASSWORD)
            admin_user.email = settings.ADMIN_INITIAL_EMAIL
            admin_user.first_name = settings.ADMIN_INITIAL_FIRST_NAME
            admin_user.last_name = settings.ADMIN_INITIAL_LAST_NAME
            admin_user.save()

        print('ok')
