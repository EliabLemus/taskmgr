"""
Phase 1 - Task CRUD Tests
"""
import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from tasks.models import Task


@pytest.fixture
def api_client():
    """Create API client"""
    return APIClient()


@pytest.fixture
def user():
    """Create test user"""
    return User.objects.create_user(
        username="testuser", password="testpass123", email="test@example.com"
    )


@pytest.fixture
def authenticated_client(api_client, user):
    """Create authenticated API client"""
    token, _ = Token.objects.get_or_create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return api_client


@pytest.fixture
def other_user():
    """Create another test user"""
    return User.objects.create_user(username="otheruser", password="otherpass123")


@pytest.mark.django_db
class TestTaskCreation:
    """Test task creation"""

    def test_create_task_success(self, authenticated_client, user):
        """Test creating a task successfully"""
        data = {
            "title": "Test Task",
            "description": "Test description",
            "status": "TODO",
            "priority": "HIGH",
        }

        response = authenticated_client.post("/api/v1/tasks/", data, format="json")

        assert response.status_code == 201
        assert response.data["title"] == "Test Task"
        assert response.data["status"] == "TODO"
        assert response.data["priority"] == "HIGH"

        # Verify task was created in database
        assert Task.objects.filter(title="Test Task", owner=user).exists()

    def test_create_task_without_auth(self, api_client):
        """Test creating task without authentication fails"""
        data = {"title": "Test Task"}

        response = api_client.post("/api/v1/tasks/", data, format="json")
        assert response.status_code == 401

    def test_create_task_missing_title(self, authenticated_client):
        """Test creating task without title fails"""
        data = {"description": "No title"}

        response = authenticated_client.post("/api/v1/tasks/", data, format="json")
        assert response.status_code == 400

    def test_create_task_invalid_status(self, authenticated_client):
        """Test creating task with invalid status fails"""
        data = {"title": "Test Task", "status": "INVALID_STATUS"}

        response = authenticated_client.post("/api/v1/tasks/", data, format="json")
        assert response.status_code == 400

    def test_create_task_minimal_data(self, authenticated_client, user):
        """Test creating task with only required fields"""
        data = {"title": "Minimal Task"}

        response = authenticated_client.post("/api/v1/tasks/", data, format="json")

        assert response.status_code == 201
        assert response.data["title"] == "Minimal Task"
        assert response.data["status"] == "TODO"  # Default
        assert response.data["priority"] == "MEDIUM"  # Default


@pytest.mark.django_db
class TestTaskRetrieval:
    """Test task retrieval"""

    def test_list_tasks(self, authenticated_client, user):
        """Test listing user's tasks"""
        # Create tasks
        Task.objects.create(title="Task 1", owner=user, status="TODO")
        Task.objects.create(title="Task 2", owner=user, status="DONE")

        response = authenticated_client.get("/api/v1/tasks/")

        assert response.status_code == 200
        assert len(response.data["results"]) == 2

    def test_list_tasks_only_own(self, authenticated_client, user, other_user):
        """Test user only sees their own tasks"""
        Task.objects.create(title="My Task", owner=user)
        Task.objects.create(title="Other Task", owner=other_user)

        response = authenticated_client.get("/api/v1/tasks/")

        assert response.status_code == 200
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["title"] == "My Task"

    def test_retrieve_task_detail(self, authenticated_client, user):
        """Test retrieving task detail"""
        task = Task.objects.create(
            title="Detailed Task",
            description="Full description",
            owner=user,
            status="IN_PROGRESS",
            priority="HIGH",
        )

        response = authenticated_client.get(f"/api/v1/tasks/{task.id}/")

        assert response.status_code == 200
        assert response.data["title"] == "Detailed Task"
        assert response.data["description"] == "Full description"
        assert "owner" in response.data

    def test_retrieve_other_user_task_fails(self, authenticated_client, other_user):
        """Test cannot retrieve another user's task"""
        task = Task.objects.create(title="Other Task", owner=other_user)

        response = authenticated_client.get(f"/api/v1/tasks/{task.id}/")
        assert response.status_code == 404


@pytest.mark.django_db
class TestTaskUpdate:
    """Test task updates"""

    def test_update_task_patch(self, authenticated_client, user):
        """Test partial update (PATCH)"""
        task = Task.objects.create(title="Original Title", owner=user, status="TODO")

        data = {"status": "IN_PROGRESS"}
        response = authenticated_client.patch(
            f"/api/v1/tasks/{task.id}/", data, format="json"
        )

        assert response.status_code == 200
        assert response.data["status"] == "IN_PROGRESS"
        assert response.data["title"] == "Original Title"  # Unchanged

        # Verify in database
        task.refresh_from_db()
        assert task.status == "IN_PROGRESS"

    def test_update_task_put(self, authenticated_client, user):
        """Test full update (PUT)"""
        task = Task.objects.create(title="Original", owner=user, status="TODO")

        data = {"title": "Updated Title", "status": "DONE", "priority": "LOW"}

        response = authenticated_client.put(
            f"/api/v1/tasks/{task.id}/", data, format="json"
        )

        assert response.status_code == 200
        assert response.data["title"] == "Updated Title"
        assert response.data["status"] == "DONE"

    def test_update_other_user_task_fails(self, authenticated_client, other_user):
        """Test cannot update another user's task"""
        task = Task.objects.create(title="Other Task", owner=other_user)

        data = {"title": "Hacked"}
        response = authenticated_client.patch(
            f"/api/v1/tasks/{task.id}/", data, format="json"
        )

        assert response.status_code == 404


@pytest.mark.django_db
class TestTaskDeletion:
    """Test task deletion"""

    def test_delete_task(self, authenticated_client, user):
        """Test deleting a task"""
        task = Task.objects.create(title="To Delete", owner=user)

        response = authenticated_client.delete(f"/api/v1/tasks/{task.id}/")

        assert response.status_code == 204
        assert not Task.objects.filter(id=task.id).exists()

    def test_delete_other_user_task_fails(self, authenticated_client, other_user):
        """Test cannot delete another user's task"""
        task = Task.objects.create(title="Other Task", owner=other_user)

        response = authenticated_client.delete(f"/api/v1/tasks/{task.id}/")
        assert response.status_code == 404
        assert Task.objects.filter(id=task.id).exists()  # Still exists


@pytest.mark.django_db
class TestCustomActions:
    """Test custom task actions"""

    def test_mark_done_action(self, authenticated_client, user):
        """Test mark_done custom action"""
        task = Task.objects.create(
            title="In Progress Task", owner=user, status="IN_PROGRESS"
        )

        response = authenticated_client.post(f"/api/v1/tasks/{task.id}/mark_done/")

        assert response.status_code == 200
        assert response.data["status"] == "DONE"

        task.refresh_from_db()
        assert task.status == "DONE"

    def test_stats_action(self, authenticated_client, user):
        """Test stats custom action"""
        # Create various tasks
        Task.objects.create(title="Task 1", owner=user, status="TODO", priority="HIGH")
        Task.objects.create(
            title="Task 2", owner=user, status="IN_PROGRESS", priority="LOW"
        )
        Task.objects.create(
            title="Task 3", owner=user, status="DONE", priority="MEDIUM"
        )

        response = authenticated_client.get("/api/v1/tasks/stats/")

        assert response.status_code == 200
        assert response.data["total"] == 3
        assert response.data["by_status"]["todo"] == 1
        assert response.data["by_status"]["in_progress"] == 1
        assert response.data["by_status"]["done"] == 1
        assert response.data["by_priority"]["high"] == 1
        assert response.data["by_priority"]["medium"] == 1
        assert response.data["by_priority"]["low"] == 1
