"""Tests for recruitment models."""
import pytest
from django.utils import timezone

from recruitment.models import JobPosition, Candidate


@pytest.mark.django_db
class TestJobPosition:
    """JobPosition model tests."""

    def test_create(self, job_position):
        """Test JobPosition creation."""
        assert job_position.pk is not None
        assert job_position.is_deleted is False

    def test_str(self, job_position):
        """Test string representation."""
        assert str(job_position) is not None
        assert len(str(job_position)) > 0

    def test_soft_delete(self, job_position):
        """Test soft delete."""
        pk = job_position.pk
        job_position.is_deleted = True
        job_position.deleted_at = timezone.now()
        job_position.save()
        assert not JobPosition.objects.filter(pk=pk).exists()
        assert JobPosition.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, job_position):
        """Test default queryset excludes deleted."""
        job_position.is_deleted = True
        job_position.deleted_at = timezone.now()
        job_position.save()
        assert JobPosition.objects.filter(hub_id=hub_id).count() == 0

    def test_toggle_active(self, job_position):
        """Test toggling is_active."""
        original = job_position.is_active
        job_position.is_active = not original
        job_position.save()
        job_position.refresh_from_db()
        assert job_position.is_active != original


@pytest.mark.django_db
class TestCandidate:
    """Candidate model tests."""

    def test_create(self, candidate):
        """Test Candidate creation."""
        assert candidate.pk is not None
        assert candidate.is_deleted is False

    def test_str(self, candidate):
        """Test string representation."""
        assert str(candidate) is not None
        assert len(str(candidate)) > 0

    def test_soft_delete(self, candidate):
        """Test soft delete."""
        pk = candidate.pk
        candidate.is_deleted = True
        candidate.deleted_at = timezone.now()
        candidate.save()
        assert not Candidate.objects.filter(pk=pk).exists()
        assert Candidate.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, candidate):
        """Test default queryset excludes deleted."""
        candidate.is_deleted = True
        candidate.deleted_at = timezone.now()
        candidate.save()
        assert Candidate.objects.filter(hub_id=hub_id).count() == 0


