from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, UserRegistrationView
from .views_metrics import metrics_summary
from .views_alerts import AlertViewSet

router = DefaultRouter()
router.register("tasks", TaskViewSet, basename="task")
router.register("alerts", AlertViewSet, basename="alert")

urlpatterns = [
    path("auth/register/", UserRegistrationView.as_view(), name="register"),
    path("metrics/summary/", metrics_summary, name="metrics-summary"),
    path("", include(router.urls)),
]
