from django.apps import AppConfig
import os  # Import the os module

class CoachSiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Coach_Site'

    def ready(self):
        # The following code will only be executed when the server is run
        # This prevents issues with makemigrations and other management commands

        from . import signals
        from . import admin
