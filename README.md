# Recruitment

## Overview

| Property | Value |
|----------|-------|
| **Module ID** | `recruitment` |
| **Version** | `1.0.0` |
| **Icon** | `person-add-outline` |
| **Dependencies** | None |

## Models

### `JobPosition`

JobPosition(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, title, department, description, status, vacancies, is_active)

| Field | Type | Details |
|-------|------|---------|
| `title` | CharField | max_length=255 |
| `department` | CharField | max_length=100, optional |
| `description` | TextField | optional |
| `status` | CharField | max_length=20, choices: draft, open, closed, on_hold |
| `vacancies` | PositiveIntegerField |  |
| `is_active` | BooleanField |  |

### `Candidate`

Candidate(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, position, name, email, phone, stage, resume_notes, rating)

| Field | Type | Details |
|-------|------|---------|
| `position` | ForeignKey | → `recruitment.JobPosition`, on_delete=CASCADE |
| `name` | CharField | max_length=255 |
| `email` | EmailField | max_length=254, optional |
| `phone` | CharField | max_length=50, optional |
| `stage` | CharField | max_length=20, choices: applied, screening, interview, offer, hired, rejected |
| `resume_notes` | TextField | optional |
| `rating` | PositiveIntegerField |  |

## Cross-Module Relationships

| From | Field | To | on_delete | Nullable |
|------|-------|----|-----------|----------|
| `Candidate` | `position` | `recruitment.JobPosition` | CASCADE | No |

## URL Endpoints

Base path: `/m/recruitment/`

| Path | Name | Method |
|------|------|--------|
| `(root)` | `dashboard` | GET |
| `positions/` | `positions` | GET |
| `job_positions/` | `job_positions_list` | GET |
| `job_positions/add/` | `job_position_add` | GET/POST |
| `job_positions/<uuid:pk>/edit/` | `job_position_edit` | GET |
| `job_positions/<uuid:pk>/delete/` | `job_position_delete` | GET/POST |
| `job_positions/<uuid:pk>/toggle/` | `job_position_toggle_status` | GET |
| `job_positions/bulk/` | `job_positions_bulk_action` | GET/POST |
| `candidates/` | `candidates_list` | GET |
| `candidates/add/` | `candidate_add` | GET/POST |
| `candidates/<uuid:pk>/edit/` | `candidate_edit` | GET |
| `candidates/<uuid:pk>/delete/` | `candidate_delete` | GET/POST |
| `candidates/bulk/` | `candidates_bulk_action` | GET/POST |
| `settings/` | `settings` | GET |

## Permissions

| Permission | Description |
|------------|-------------|
| `recruitment.view_jobposition` | View Jobposition |
| `recruitment.add_jobposition` | Add Jobposition |
| `recruitment.change_jobposition` | Change Jobposition |
| `recruitment.delete_jobposition` | Delete Jobposition |
| `recruitment.view_candidate` | View Candidate |
| `recruitment.add_candidate` | Add Candidate |
| `recruitment.change_candidate` | Change Candidate |
| `recruitment.manage_settings` | Manage Settings |

**Role assignments:**

- **admin**: All permissions
- **manager**: `add_candidate`, `add_jobposition`, `change_candidate`, `change_jobposition`, `view_candidate`, `view_jobposition`
- **employee**: `add_jobposition`, `view_candidate`, `view_jobposition`

## Navigation

| View | Icon | ID | Fullpage |
|------|------|----|----------|
| Dashboard | `speedometer-outline` | `dashboard` | No |
| Positions | `briefcase-outline` | `positions` | No |
| Candidates | `person-add-outline` | `candidates` | No |
| Settings | `settings-outline` | `settings` | No |

## AI Tools

Tools available for the AI assistant:

### `list_job_positions`

List job positions/openings.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `status` | string | No | draft, open, closed, on_hold |
| `department` | string | No |  |

### `create_job_position`

Create a job position/opening.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `title` | string | Yes |  |
| `department` | string | No |  |
| `description` | string | No |  |
| `vacancies` | integer | No |  |

### `list_candidates`

List job candidates.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `position_id` | string | No |  |
| `stage` | string | No | applied, screening, interview, offer, hired, rejected |
| `limit` | integer | No |  |

### `create_candidate`

Add a candidate to a job position.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `position_id` | string | Yes |  |
| `name` | string | Yes |  |
| `email` | string | No |  |
| `phone` | string | No |  |
| `resume_notes` | string | No |  |

## File Structure

```
README.md
__init__.py
admin.py
ai_tools.py
apps.py
forms.py
locale/
  en/
    LC_MESSAGES/
      django.po
  es/
    LC_MESSAGES/
      django.po
migrations/
  0001_initial.py
  __init__.py
models.py
module.py
static/
  icons/
    icon.svg
  recruitment/
    css/
    js/
templates/
  recruitment/
    pages/
      candidate_add.html
      candidate_edit.html
      candidates.html
      dashboard.html
      index.html
      job_position_add.html
      job_position_edit.html
      job_positions.html
      positions.html
      settings.html
    partials/
      candidate_add_content.html
      candidate_edit_content.html
      candidates_content.html
      candidates_list.html
      dashboard_content.html
      job_position_add_content.html
      job_position_edit_content.html
      job_positions_content.html
      job_positions_list.html
      panel_candidate_add.html
      panel_candidate_edit.html
      panel_job_position_add.html
      panel_job_position_edit.html
      positions_content.html
      settings_content.html
tests/
  __init__.py
  conftest.py
  test_models.py
  test_views.py
urls.py
views.py
```
