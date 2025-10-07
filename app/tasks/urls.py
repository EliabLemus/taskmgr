"""
URL configuration for tasks app
"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TaskViewSet, UserRegistrationView

# Create router for ViewSets
router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="task")

urlpatterns = [
    # User registration
    path("auth/register/", UserRegistrationView.as_view(), name="user-register"),
    # Task endpoints (via router)
    path("", include(router.urls)),
]
