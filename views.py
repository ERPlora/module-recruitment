"""
Recruitment Module Views
"""
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, render as django_render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from apps.accounts.decorators import login_required
from apps.core.htmx import htmx_view
from apps.core.services import export_to_csv, export_to_excel
from apps.modules_runtime.navigation import with_module_nav

from .models import JobPosition, Candidate

PER_PAGE_CHOICES = [10, 25, 50, 100]


# ======================================================================
# Dashboard
# ======================================================================

@login_required
@with_module_nav('recruitment', 'dashboard')
@htmx_view('recruitment/pages/index.html', 'recruitment/partials/dashboard_content.html')
def dashboard(request):
    hub_id = request.session.get('hub_id')
    return {
        'total_job_positions': JobPosition.objects.filter(hub_id=hub_id, is_deleted=False).count(),
        'total_candidates': Candidate.objects.filter(hub_id=hub_id, is_deleted=False).count(),
    }


# ======================================================================
# JobPosition
# ======================================================================

JOB_POSITION_SORT_FIELDS = {
    'title': 'title',
    'status': 'status',
    'is_active': 'is_active',
    'vacancies': 'vacancies',
    'department': 'department',
    'description': 'description',
    'created_at': 'created_at',
}

def _build_job_positions_context(hub_id, per_page=10):
    qs = JobPosition.objects.filter(hub_id=hub_id, is_deleted=False).order_by('title')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'job_positions': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'title',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_job_positions_list(request, hub_id, per_page=10):
    ctx = _build_job_positions_context(hub_id, per_page)
    return django_render(request, 'recruitment/partials/job_positions_list.html', ctx)

@login_required
@with_module_nav('recruitment', 'positions')
@htmx_view('recruitment/pages/job_positions.html', 'recruitment/partials/job_positions_content.html')
def job_positions_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'title')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = JobPosition.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(title__icontains=search_query) | Q(department__icontains=search_query) | Q(description__icontains=search_query) | Q(status__icontains=search_query))

    order_by = JOB_POSITION_SORT_FIELDS.get(sort_field, 'title')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['title', 'status', 'is_active', 'vacancies', 'department', 'description']
        headers = ['Title', 'Status', 'Is Active', 'Vacancies', 'Department', 'Description']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='job_positions.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='job_positions.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'recruitment/partials/job_positions_list.html', {
            'job_positions': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'job_positions': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def job_position_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        department = request.POST.get('department', '').strip()
        description = request.POST.get('description', '').strip()
        status = request.POST.get('status', '').strip()
        vacancies = int(request.POST.get('vacancies', 0) or 0)
        is_active = request.POST.get('is_active') == 'on'
        obj = JobPosition(hub_id=hub_id)
        obj.title = title
        obj.department = department
        obj.description = description
        obj.status = status
        obj.vacancies = vacancies
        obj.is_active = is_active
        obj.save()
        return _render_job_positions_list(request, hub_id)
    return django_render(request, 'recruitment/partials/panel_job_position_add.html', {})

@login_required
def job_position_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(JobPosition, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.title = request.POST.get('title', '').strip()
        obj.department = request.POST.get('department', '').strip()
        obj.description = request.POST.get('description', '').strip()
        obj.status = request.POST.get('status', '').strip()
        obj.vacancies = int(request.POST.get('vacancies', 0) or 0)
        obj.is_active = request.POST.get('is_active') == 'on'
        obj.save()
        return _render_job_positions_list(request, hub_id)
    return django_render(request, 'recruitment/partials/panel_job_position_edit.html', {'obj': obj})

@login_required
@require_POST
def job_position_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(JobPosition, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_job_positions_list(request, hub_id)

@login_required
@require_POST
def job_position_toggle_status(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(JobPosition, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_active = not obj.is_active
    obj.save(update_fields=['is_active', 'updated_at'])
    return _render_job_positions_list(request, hub_id)

@login_required
@require_POST
def job_positions_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = JobPosition.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'activate':
        qs.update(is_active=True)
    elif action == 'deactivate':
        qs.update(is_active=False)
    elif action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_job_positions_list(request, hub_id)


# ======================================================================
# Candidate
# ======================================================================

CANDIDATE_SORT_FIELDS = {
    'name': 'name',
    'position': 'position',
    'stage': 'stage',
    'rating': 'rating',
    'email': 'email',
    'phone': 'phone',
    'created_at': 'created_at',
}

def _build_candidates_context(hub_id, per_page=10):
    qs = Candidate.objects.filter(hub_id=hub_id, is_deleted=False).order_by('name')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'candidates': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'name',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_candidates_list(request, hub_id, per_page=10):
    ctx = _build_candidates_context(hub_id, per_page)
    return django_render(request, 'recruitment/partials/candidates_list.html', ctx)

@login_required
@with_module_nav('recruitment', 'candidates')
@htmx_view('recruitment/pages/candidates.html', 'recruitment/partials/candidates_content.html')
def candidates_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'name')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = Candidate.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(name__icontains=search_query) | Q(email__icontains=search_query) | Q(phone__icontains=search_query) | Q(stage__icontains=search_query))

    order_by = CANDIDATE_SORT_FIELDS.get(sort_field, 'name')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['name', 'position', 'stage', 'rating', 'email', 'phone']
        headers = ['Name', 'JobPosition', 'Stage', 'Rating', 'Email', 'Phone']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='candidates.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='candidates.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'recruitment/partials/candidates_list.html', {
            'candidates': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'candidates': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def candidate_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        stage = request.POST.get('stage', '').strip()
        resume_notes = request.POST.get('resume_notes', '').strip()
        rating = int(request.POST.get('rating', 0) or 0)
        obj = Candidate(hub_id=hub_id)
        obj.name = name
        obj.email = email
        obj.phone = phone
        obj.stage = stage
        obj.resume_notes = resume_notes
        obj.rating = rating
        obj.save()
        return _render_candidates_list(request, hub_id)
    return django_render(request, 'recruitment/partials/panel_candidate_add.html', {})

@login_required
def candidate_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Candidate, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '').strip()
        obj.email = request.POST.get('email', '').strip()
        obj.phone = request.POST.get('phone', '').strip()
        obj.stage = request.POST.get('stage', '').strip()
        obj.resume_notes = request.POST.get('resume_notes', '').strip()
        obj.rating = int(request.POST.get('rating', 0) or 0)
        obj.save()
        return _render_candidates_list(request, hub_id)
    return django_render(request, 'recruitment/partials/panel_candidate_edit.html', {'obj': obj})

@login_required
@require_POST
def candidate_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Candidate, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_candidates_list(request, hub_id)

@login_required
@require_POST
def candidates_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = Candidate.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_candidates_list(request, hub_id)


@login_required
@with_module_nav('recruitment', 'settings')
@htmx_view('recruitment/pages/settings.html', 'recruitment/partials/settings_content.html')
def settings_view(request):
    return {}

