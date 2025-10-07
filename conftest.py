"""
Pytest configuration for Task Manager API tests
"""
import sys
from pathlib import Path

# Add project root and app directory to Python path
project_root = Path(__file__).parent
app_dir = project_root / 'app'

sys.path.insert(0, str(project_root))
sys.path.insert(0, str(app_dir))

# Set Django settings module
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

# Setup Django
import django
django.setup()
