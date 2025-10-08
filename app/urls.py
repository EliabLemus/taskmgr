from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from app.tasks.views_health import health_check, status_check

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # Health & Status (no /api/v1/ prefix)
    path("health", health_check, name="health"),
    path("status", status_check, name="status"),
    # API v1 - Tasks and Alerts
    path("api/v1/", include("app.tasks.urls")),
    # API v1 - Token authentication
    path("api/v1/auth/token/", obtain_auth_token, name="api_token_auth"),
    # API Documentation
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/v1/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/v1/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
    ),
    # Prometheus metrics
    path("", include("django_prometheus.urls")),
]
