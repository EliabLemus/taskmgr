"""
Phase 1 - Filtering, Search, and Ordering Tests
"""
from datetime import timedelta

import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from tasks.models import Task


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", password="testpass")


@pytest.fixture
def authenticated_client(api_client, user):
    token, _ = Token.objects.get_or_create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return api_client


@pytest.mark.django_db
class TestFiltering:
    """Test task filtering"""

    def test_filter_by_status(self, authenticated_client, user):
        """Test filtering tasks by status"""
        Task.objects.create(title="Todo Task", owner=user, status="TODO")
        Task.objects.create(title="Done Task", owner=user, status="DONE")
        Task.objects.create(title="In Progress", owner=user, status="IN_PROGRESS")

        response = authenticated_client.get("/api/v1/tasks/?status=TODO")

        assert response.status_code == 200
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["status"] == "TODO"

    def test_filter_by_priority(self, authenticated_client, user):
        """Test filtering tasks by priority"""
        Task.objects.create(title="High Task", owner=user, priority="HIGH")
        Task.objects.create(title="Low Task", owner=user, priority="LOW")
        Task.objects.create(title="Medium Task", owner=user, priority="MEDIUM")

        response = authenticated_client.get("/api/v1/tasks/?priority=HIGH")

        assert response.status_code == 200
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["priority"] == "HIGH"

    def test_filter_multiple_params(self, authenticated_client, user):
        """Test filtering with multiple parameters"""
        Task.objects.create(title="Task 1", owner=user, status="TODO", priority="HIGH")
        Task.objects.create(title="Task 2", owner=user, status="TODO", priority="LOW")
        Task.objects.create(title="Task 3", owner=user, status="DONE", priority="HIGH")

        response = authenticated_client.get("/api/v1/tasks/?status=TODO&priority=HIGH")

        assert response.status_code == 200
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["title"] == "Task 1"


@pytest.mark.django_db
class TestSearch:
    """Test task search"""

    def test_search_by_title(self, authenticated_client, user):
        """Test searching tasks by title"""
        Task.objects.create(title="Deploy to production", owner=user)
        Task.objects.create(title="Write tests", owner=user)
        Task.objects.create(title="Deploy to staging", owner=user)

        response = authenticated_client.get("/api/v1/tasks/?search=deploy")

        assert response.status_code == 200
        assert len(response.data["results"]) == 2

    def test_search_by_description(self, authenticated_client, user):
        """Test searching tasks by description"""
        Task.objects.create(
            title="Task 1", description="Contains urgent keyword", owner=user
        )
        Task.objects.create(title="Task 2", description="Normal task", owner=user)

        response = authenticated_client.get("/api/v1/tasks/?search=urgent")

        assert response.status_code == 200
        assert len(response.data["results"]) == 1

    def test_search_case_insensitive(self, authenticated_client, user):
        """Test search is case insensitive"""
        Task.objects.create(title="URGENT Task", owner=user)

        response = authenticated_client.get("/api/v1/tasks/?search=urgent")

        assert response.status_code == 200
        assert len(response.data["results"]) == 1


@pytest.mark.django_db
class TestOrdering:
    """Test task ordering"""

    def test_order_by_created_at_desc(self, authenticated_client, user):
        """Test ordering by created_at descending (default)"""
        task1 = Task.objects.create(title="First", owner=user)
        task2 = Task.objects.create(title="Second", owner=user)
        task3 = Task.objects.create(title="Third", owner=user)

        response = authenticated_client.get("/api/v1/tasks/")

        assert response.status_code == 200
        results = response.data["results"]
        assert results[0]["title"] == "Third"  # Most recent first
        assert results[2]["title"] == "First"

    def test_order_by_priority(self, authenticated_client, user):
        """Test ordering by priority"""
        Task.objects.create(title="Low", owner=user, priority="LOW")
        Task.objects.create(title="High", owner=user, priority="HIGH")
        Task.objects.create(title="Medium", owner=user, priority="MEDIUM")

        response = authenticated_client.get("/api/v1/tasks/?ordering=priority")

        assert response.status_code == 200
        # Ordering will be alphabetical: HIGH, LOW, MEDIUM
        results = response.data["results"]
        assert len(results) == 3


@pytest.mark.django_db
class TestPagination:
    """Test pagination"""

    def test_pagination_default_page_size(self, authenticated_client, user):
        """Test default pagination page size"""
        # Create 25 tasks (more than default page size of 20)
        for i in range(25):
            Task.objects.create(title=f"Task {i}", owner=user)

        response = authenticated_client.get("/api/v1/tasks/")

        assert response.status_code == 200
        assert len(response.data["results"]) == 20  # Default page size
        assert response.data["count"] == 25
        assert response.data["next"] is not None

    def test_pagination_custom_page_size(self, authenticated_client, user):
        """Test custom page size"""
        for i in range(15):
            Task.objects.create(title=f"Task {i}", owner=user)

        response = authenticated_client.get("/api/v1/tasks/?page_size=5")

        assert response.status_code == 200
        assert len(response.data["results"]) == 5
        assert response.data["count"] == 15

    def test_pagination_page_2(self, authenticated_client, user):
        """Test accessing page 2"""
        for i in range(25):
            Task.objects.create(title=f"Task {i}", owner=user)

        response = authenticated_client.get("/api/v1/tasks/?page=2")

        assert response.status_code == 200
        assert len(response.data["results"]) == 5  # Remaining tasks
        assert response.data["previous"] is not None
