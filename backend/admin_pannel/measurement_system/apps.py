from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'measurement_system'
    verbose_name = _("Measurement system database")
