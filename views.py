"""
Recruitment Module Views
"""
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.accounts.decorators import login_required
from apps.core.htmx import htmx_view
from apps.modules_runtime.navigation import with_module_nav


@login_required
@with_module_nav('recruitment', 'dashboard')
@htmx_view('recruitment/pages/dashboard.html', 'recruitment/partials/dashboard_content.html')
def dashboard(request):
    """Dashboard view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('recruitment', 'positions')
@htmx_view('recruitment/pages/positions.html', 'recruitment/partials/positions_content.html')
def positions(request):
    """Positions view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('recruitment', 'candidates')
@htmx_view('recruitment/pages/candidates.html', 'recruitment/partials/candidates_content.html')
def candidates(request):
    """Candidates view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('recruitment', 'settings')
@htmx_view('recruitment/pages/settings.html', 'recruitment/partials/settings_content.html')
def settings(request):
    """Settings view."""
    hub_id = request.session.get('hub_id')
    return {}

