"""Tests for recruitment views."""
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestDashboard:
    """Dashboard view tests."""

    def test_dashboard_loads(self, auth_client):
        """Test dashboard page loads."""
        url = reverse('recruitment:dashboard')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_dashboard_htmx(self, auth_client):
        """Test dashboard HTMX partial."""
        url = reverse('recruitment:dashboard')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_dashboard_requires_auth(self, client):
        """Test dashboard requires authentication."""
        url = reverse('recruitment:dashboard')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestJobPositionViews:
    """JobPosition view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('recruitment:job_positions_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('recruitment:job_positions_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('recruitment:job_positions_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('recruitment:job_positions_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('recruitment:job_positions_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('recruitment:job_positions_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('recruitment:job_position_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('recruitment:job_position_add')
        data = {
            'title': 'New Title',
            'department': 'New Department',
            'description': 'Test description',
            'status': 'New Status',
            'vacancies': '5',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, job_position):
        """Test edit form loads."""
        url = reverse('recruitment:job_position_edit', args=[job_position.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, job_position):
        """Test editing via POST."""
        url = reverse('recruitment:job_position_edit', args=[job_position.pk])
        data = {
            'title': 'Updated Title',
            'department': 'Updated Department',
            'description': 'Test description',
            'status': 'Updated Status',
            'vacancies': '5',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, job_position):
        """Test soft delete via POST."""
        url = reverse('recruitment:job_position_delete', args=[job_position.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        job_position.refresh_from_db()
        assert job_position.is_deleted is True

    def test_toggle_status(self, auth_client, job_position):
        """Test toggle active status."""
        url = reverse('recruitment:job_position_toggle_status', args=[job_position.pk])
        original = job_position.is_active
        response = auth_client.post(url)
        assert response.status_code == 200
        job_position.refresh_from_db()
        assert job_position.is_active != original

    def test_bulk_delete(self, auth_client, job_position):
        """Test bulk delete."""
        url = reverse('recruitment:job_positions_bulk_action')
        response = auth_client.post(url, {'ids': str(job_position.pk), 'action': 'delete'})
        assert response.status_code == 200
        job_position.refresh_from_db()
        assert job_position.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('recruitment:job_positions_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestCandidateViews:
    """Candidate view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('recruitment:candidates_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('recruitment:candidates_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('recruitment:candidates_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('recruitment:candidates_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('recruitment:candidates_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('recruitment:candidates_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('recruitment:candidate_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('recruitment:candidate_add')
        data = {
            'name': 'New Name',
            'email': 'test@example.com',
            'phone': 'New Phone',
            'stage': 'New Stage',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, candidate):
        """Test edit form loads."""
        url = reverse('recruitment:candidate_edit', args=[candidate.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, candidate):
        """Test editing via POST."""
        url = reverse('recruitment:candidate_edit', args=[candidate.pk])
        data = {
            'name': 'Updated Name',
            'email': 'test@example.com',
            'phone': 'Updated Phone',
            'stage': 'Updated Stage',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, candidate):
        """Test soft delete via POST."""
        url = reverse('recruitment:candidate_delete', args=[candidate.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        candidate.refresh_from_db()
        assert candidate.is_deleted is True

    def test_bulk_delete(self, auth_client, candidate):
        """Test bulk delete."""
        url = reverse('recruitment:candidates_bulk_action')
        response = auth_client.post(url, {'ids': str(candidate.pk), 'action': 'delete'})
        assert response.status_code == 200
        candidate.refresh_from_db()
        assert candidate.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('recruitment:candidates_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestSettings:
    """Settings view tests."""

    def test_settings_loads(self, auth_client):
        """Test settings page loads."""
        url = reverse('recruitment:settings')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_settings_requires_auth(self, client):
        """Test settings requires authentication."""
        url = reverse('recruitment:settings')
        response = client.get(url)
        assert response.status_code == 302

