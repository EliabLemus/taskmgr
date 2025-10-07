from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def health_check(request):
    return JsonResponse({'status': 'healthy', 'service': 'taskmgr-api'})

def status_check(request):
    return JsonResponse({
        'status': 'operational',
        'version': '1.0.0',
        'api_version': 'v1'
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health', health_check),
    path('status', status_check),
    path('', include('django_prometheus.urls')),
]
