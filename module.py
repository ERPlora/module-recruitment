from django.utils.translation import gettext_lazy as _

MODULE_ID = 'recruitment'
MODULE_NAME = _('Recruitment')
MODULE_VERSION = '1.0.0'
MODULE_ICON = 'person-add-outline'
MODULE_DESCRIPTION = _('Job postings, candidates and hiring pipeline')
MODULE_AUTHOR = 'ERPlora'
MODULE_CATEGORY = 'hr'

MENU = {
    'label': _('Recruitment'),
    'icon': 'person-add-outline',
    'order': 43,
}

NAVIGATION = [
    {'label': _('Dashboard'), 'icon': 'speedometer-outline', 'id': 'dashboard'},
{'label': _('Positions'), 'icon': 'briefcase-outline', 'id': 'positions'},
{'label': _('Candidates'), 'icon': 'person-add-outline', 'id': 'candidates'},
{'label': _('Settings'), 'icon': 'settings-outline', 'id': 'settings'},
]

DEPENDENCIES = []

PERMISSIONS = [
    'recruitment.view_jobposition',
'recruitment.add_jobposition',
'recruitment.change_jobposition',
'recruitment.delete_jobposition',
'recruitment.view_candidate',
'recruitment.add_candidate',
'recruitment.change_candidate',
'recruitment.manage_settings',
]
