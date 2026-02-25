from core.models import SiteSettings
from clinic.models import Department, Treatment


def site_settings(request):
    try:
        settings = SiteSettings.objects.first()
    except Exception:
        settings = None
    
    try:
        departments = Department.objects.filter(dept_type='deps', is_active=True)
    except Exception:
        departments = []
    
    try:
        featured_treatments = Treatment.objects.filter(is_featured=True, is_active=True)
    except Exception:
        featured_treatments = []
    
    return {
        'site_settings': settings,
        'nav_departments': departments,
        'featured_treatments': featured_treatments,
    }
