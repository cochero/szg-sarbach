from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
from .models import Banner, ContactSubmission, UserProfile
from clinic.models import Department, Treatment, Doctor, Hotel, Package, Addon
from blog_app.models import BlogPost
from appointments.models import Appointment
from shop.models import Order


def home(request):
    banners = Banner.objects.filter(is_active=True)
    departments = Department.objects.filter(dept_type='deps', is_active=True)
    symptoms = Department.objects.filter(dept_type='symptoms', is_active=True)
    treatments = Treatment.objects.filter(is_active=True)
    doctors = Doctor.objects.filter(is_active=True)[:8]
    blogs = BlogPost.objects.filter(post_type='Blog', is_active=True)[:3]
    addons = Addon.objects.filter(is_active=True)
    return render(request, 'core/home.html', {
        'banners': banners,
        'departments': departments,
        'symptoms': symptoms,
        'treatments': treatments,
        'doctors': doctors,
        'blogs': blogs,
        'addons': addons,
    })


def about(request):
    from clinic.models import Doctor
    doctors = Doctor.objects.filter(is_active=True)
    return render(request, 'core/about.html', {'doctors': doctors})


def contact(request):
    return render(request, 'core/contact.html')


@require_POST
def contact_submit(request):
    try:
        ContactSubmission.objects.create(
            name=request.POST.get('name', ''),
            email=request.POST.get('email', ''),
            phone=request.POST.get('phone', ''),
            subject=request.POST.get('subject', ''),
            message=request.POST.get('message', ''),
        )
        return JsonResponse({'success': True, 'message': 'Your enquiry has been received successfully. We will get back to you soon.'})
    except Exception:
        return JsonResponse({'success': False, 'message': 'An error occurred. Please try again.'})


def privacy(request):
    return render(request, 'core/privacy.html')


def terms(request):
    return render(request, 'core/terms.html')


def realestate(request):
    return render(request, 'core/realestate.html')


def register_page(request):
    return redirect('contact')


def patient_login(request):
    return redirect('contact')


def patient_register(request):
    return redirect('contact')


def doctor_login_page(request):
    return render(request, 'core/doctor_login.html')


def doctor_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user and hasattr(user, 'profile') and user.profile.role == 'doctor':
            login(request, user)
            return redirect('doctor_dashboard')
        messages.error(request, 'Invalid doctor credentials')
        return redirect('doctor_login_page')
    return redirect('doctor_login_page')


def admin_login_page(request):
    return render(request, 'core/admin_login.html')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user and (user.is_superuser or (hasattr(user, 'profile') and user.profile.role in ['superadmin', 'frontdesk'])):
            login(request, user)
            return redirect('admin_dashboard')
        messages.error(request, 'Invalid login credentials')
        return redirect('admin_login_page')
    return redirect('admin_login_page')


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def user_dashboard(request):
    appointments = Appointment.objects.filter(patient=request.user)
    return render(request, 'core/user_dashboard.html', {'appointments': appointments})


@login_required
def user_profile(request):
    if request.method == 'POST':
        profile = request.user.profile
        request.user.first_name = request.POST.get('first_name', request.user.first_name)
        request.user.last_name = request.POST.get('last_name', request.user.last_name)
        request.user.save()
        profile.phone = request.POST.get('phone', profile.phone)
        profile.city = request.POST.get('city', profile.city)
        profile.street = request.POST.get('street', profile.street)
        profile.plz = request.POST.get('plz', profile.plz)
        if request.FILES.get('profile_image'):
            profile.profile_image = request.FILES['profile_image']
        profile.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('user_profile')
    return render(request, 'core/user_profile.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password', '')
        new_password = request.POST.get('new_password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
        elif not new_password:
            messages.error(request, 'New password cannot be empty.')
        elif len(new_password) < 6:
            messages.error(request, 'New password must be at least 6 characters.')
        elif new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
        else:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Your password has been changed successfully. You are still logged in.')
            try:
                role = request.user.profile.role
                if role == 'doctor':
                    return redirect('doctor_dashboard')
                elif role in ('superadmin', 'frontdesk'):
                    return redirect('admin_dashboard')
            except Exception:
                pass
            return redirect('user_dashboard')
    return render(request, 'core/change_password.html')


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /panel/",
        "Disallow: /admin/",
        "Disallow: /user/",
        "Disallow: /welcome/",
        "",
        f"Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def sitemap_xml(request):
    base_url = f"{request.scheme}://{request.get_host()}"
    departments = Department.objects.filter(is_active=True)
    treatments = Treatment.objects.filter(is_active=True)
    doctors = Doctor.objects.filter(is_active=True)
    blogs = BlogPost.objects.filter(is_active=True)

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    static_pages = ['/', '/about/', '/contact/', '/packages/', '/accommodations/', '/blog/', '/events/', '/privacy/', '/terms/']
    for page in static_pages:
        xml += f'  <url><loc>{base_url}{page}</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>\n'

    for dept in departments:
        xml += f'  <url><loc>{base_url}/departments/{dept.slug}/</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>\n'

    for t in treatments:
        xml += f'  <url><loc>{base_url}/treatment/{t.slug}/</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>\n'

    for d in doctors:
        xml += f'  <url><loc>{base_url}/doctor/{d.slug}/</loc><changefreq>monthly</changefreq><priority>0.6</priority></url>\n'

    for b in blogs:
        xml += f'  <url><loc>{base_url}/blog/{b.slug}/</loc><changefreq>weekly</changefreq><priority>0.6</priority></url>\n'

    xml += '</urlset>'
    return HttpResponse(xml, content_type="application/xml")
