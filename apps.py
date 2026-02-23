from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RecruitmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recruitment'
    label = 'recruitment'
    verbose_name = _('Recruitment')

    def ready(self):
        pass
