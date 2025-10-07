"""
Main URL configuration for Task Manager API
"""
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)
from rest_framework.authtoken.views import obtain_auth_token


def health_check(request):
    """Health check endpoint"""
    return JsonResponse({"status": "healthy", "service": "taskmgr-api"})


def status_check(request):
    """Status check endpoint"""
    return JsonResponse(
        {"status": "operational", "version": "1.0.0", "api_version": "v1"}
    )


urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # Health & Status
    path("health", health_check, name="health"),
    path("status", status_check, name="status"),
    # Prometheus metrics
    path("", include("django_prometheus.urls")),
    # API v1
    path(
        "api/v1/",
        include(
            [
                # Authentication
                path("auth/token/", obtain_auth_token, name="api-token-auth"),
                # Tasks & User Registration
                path("", include("tasks.urls")),
                # API Documentation
                path("schema/", SpectacularAPIView.as_view(), name="schema"),
                path(
                    "docs/",
                    SpectacularSwaggerView.as_view(url_name="schema"),
                    name="swagger-ui",
                ),
                path(
                    "redoc/",
                    SpectacularRedocView.as_view(url_name="schema"),
                    name="redoc",
                ),
            ]
        ),
    ),
]
