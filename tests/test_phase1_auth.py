"""
Phase 1 - Authentication Tests
"""
import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestUserRegistration:
    """Test user registration endpoint"""

    def test_register_user_success(self):
        """Test successful user registration"""
        client = APIClient()

        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "securepass123",
            "first_name": "Test",
            "last_name": "User",
        }

        response = client.post("/api/v1/auth/register/", data, format="json")

        assert response.status_code == 201
        assert "user" in response.data
        assert "token" in response.data
        assert response.data["user"]["username"] == "testuser"
        assert response.data["user"]["email"] == "test@example.com"

        # Verify user was created
        assert User.objects.filter(username="testuser").exists()

    def test_register_duplicate_username(self):
        """Test registration with duplicate username fails"""
        User.objects.create_user(username="existing", password="pass123")

        client = APIClient()
        data = {"username": "existing", "password": "newpass123"}

        response = client.post("/api/v1/auth/register/", data, format="json")
        assert response.status_code == 400

    def test_register_missing_username(self):
        """Test registration without username fails"""
        client = APIClient()
        data = {"password": "pass123"}

        response = client.post("/api/v1/auth/register/", data, format="json")
        assert response.status_code == 400

    def test_register_missing_password(self):
        """Test registration without password fails"""
        client = APIClient()
        data = {"username": "testuser"}

        response = client.post("/api/v1/auth/register/", data, format="json")
        assert response.status_code == 400


@pytest.mark.django_db
class TestTokenAuthentication:
    """Test token authentication endpoint"""

    def test_obtain_token_success(self):
        """Test obtaining token with valid credentials"""
        user = User.objects.create_user(username="testuser", password="testpass123")

        client = APIClient()
        data = {"username": "testuser", "password": "testpass123"}

        response = client.post("/api/v1/auth/token/", data, format="json")

        assert response.status_code == 200
        assert "token" in response.data

        # Verify token is valid
        token = Token.objects.get(user=user)
        assert response.data["token"] == token.key

    def test_obtain_token_invalid_password(self):
        """Test token request with wrong password fails"""
        User.objects.create_user(username="testuser", password="correctpass")

        client = APIClient()
        data = {"username": "testuser", "password": "wrongpass"}

        response = client.post("/api/v1/auth/token/", data, format="json")
        assert response.status_code == 400

    def test_obtain_token_nonexistent_user(self):
        """Test token request for non-existent user fails"""
        client = APIClient()
        data = {"username": "nonexistent", "password": "pass123"}

        response = client.post("/api/v1/auth/token/", data, format="json")
        assert response.status_code == 400
