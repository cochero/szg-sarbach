from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Department, Treatment, Doctor, Hotel, Package, Addon, Gallery


def department_list(request, slug):
    department = get_object_or_404(Department, slug=slug, is_active=True)
    treatments = Treatment.objects.filter(department=department, is_active=True)
    return render(request, 'clinic/department.html', {
        'department': department,
        'treatments': treatments,
    })


def treatment_detail(request, slug):
    treatment = get_object_or_404(Treatment, slug=slug, is_active=True)
    gallery = Gallery.objects.filter(gallery_type='treatment', related_id=treatment.id)
    steps = treatment.steps.all()
    return render(request, 'clinic/treatment.html', {
        'treatment': treatment,
        'gallery': gallery,
        'steps': steps,
    })


def doctor_profile(request):
    doctors = Doctor.objects.filter(is_active=True)
    return render(request, 'clinic/doctor_profile.html', {'doctors': doctors})


def accommodations(request):
    hotels = Hotel.objects.filter(hotel_type='Apartment', is_active=True).select_related('city')
    return render(request, 'clinic/accommodations.html', {'accommodations': hotels})


def accommodation_detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    gallery = Gallery.objects.filter(gallery_type='hotel', related_id=hotel.id)
    other_accommodations = Hotel.objects.filter(is_active=True).exclude(pk=pk)[:3]
    return render(request, 'clinic/accommodation_detail.html', {
        'accommodation': hotel,
        'gallery': gallery,
        'other_accommodations': other_accommodations,
    })


def package_list(request):
    packages = Package.objects.filter(is_active=True)
    return render(request, 'clinic/packages.html', {'packages': packages})


def package_detail(request, slug):
    package = get_object_or_404(Package, slug=slug, is_active=True)
    return render(request, 'clinic/package_detail.html', {'package': package})


def addon_list(request):
    addons = Addon.objects.filter(is_active=True)
    return render(request, 'clinic/addons.html', {'addons': addons})


def ajax_treatments(request):
    if request.method == 'POST':
        dept_id = request.POST.get('dept')
        treatments = Treatment.objects.filter(department_id=dept_id, is_active=True)
        html = ''
        for t in treatments:
            html += f'<option value="{t.id}">{t.name} - {t.duration_days} days @ CHF {t.price}</option>'
        return JsonResponse({'html': html})
    return JsonResponse({'html': ''})
