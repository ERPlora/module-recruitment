from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import HubBaseModel

JOB_STATUS = [
    ('draft', _('Draft')),
    ('open', _('Open')),
    ('closed', _('Closed')),
    ('on_hold', _('On Hold')),
]

CAND_STAGE = [
    ('applied', _('Applied')),
    ('screening', _('Screening')),
    ('interview', _('Interview')),
    ('offer', _('Offer')),
    ('hired', _('Hired')),
    ('rejected', _('Rejected')),
]

class JobPosition(HubBaseModel):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    department = models.CharField(max_length=100, blank=True, verbose_name=_('Department'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    status = models.CharField(max_length=20, default='open', choices=JOB_STATUS, verbose_name=_('Status'))
    vacancies = models.PositiveIntegerField(default=1, verbose_name=_('Vacancies'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))

    class Meta(HubBaseModel.Meta):
        db_table = 'recruitment_jobposition'

    def __str__(self):
        return self.title


class Candidate(HubBaseModel):
    position = models.ForeignKey('JobPosition', on_delete=models.CASCADE, related_name='candidates')
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    email = models.EmailField(blank=True, verbose_name=_('Email'))
    phone = models.CharField(max_length=50, blank=True, verbose_name=_('Phone'))
    stage = models.CharField(max_length=20, default='applied', choices=CAND_STAGE, verbose_name=_('Stage'))
    resume_notes = models.TextField(blank=True, verbose_name=_('Resume Notes'))
    rating = models.PositiveIntegerField(default=0, verbose_name=_('Rating'))

    class Meta(HubBaseModel.Meta):
        db_table = 'recruitment_candidate'

    def __str__(self):
        return self.name

