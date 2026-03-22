from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from datetime import datetime
from .models import Appointment, Examination, AddonOrder, AppointmentDiet, PatientRecord
from clinic.models import Department, Treatment, Doctor, City, Hotel
from core.models import UserProfile


def appointment_page(request):
    from django.shortcuts import redirect as redir
    return redir('contact')


@login_required
def appointment_submit(request):
    if request.method == 'POST':
        try:
            app_date_str = request.POST.get('app_date', '')
            try:
                app_date = datetime.strptime(app_date_str, '%d/%m/%Y').date()
            except ValueError:
                try:
                    app_date = datetime.strptime(app_date_str, '%Y-%m-%d').date()
                except ValueError:
                    app_date = datetime.now().date()

            appointment = Appointment.objects.create(
                patient=request.user,
                appointment_date=app_date,
                appointment_time=request.POST.get('app_time', None) or None,
                amount=request.POST.get('app_amt', 0) or 0,
                city_id=request.POST.get('app_city') or None,
                location_id=request.POST.get('app_location') or None,
                appointment_type=request.POST.get('app_type', 'Walkin'),
                description=request.POST.get('app_desc', ''),
                department_id=request.POST.get('app_dept') or None,
                treatment_id=request.POST.get('app_treat') or None,
                payment_status=request.POST.get('app_payment', 'Pending'),
                status=request.POST.get('app_status', 'Pending'),
                created_by=request.POST.get('app_created', 'Patient'),
            )
            return JsonResponse({'success': True, 'id': appointment.id})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request'})


@login_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'appointments/appointment_detail.html', {'appointment': appointment})


@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(patient=request.user)
    return render(request, 'appointments/my_appointments.html', {'appointments': appointments})


@login_required
def my_addons(request):
    addon_orders = AddonOrder.objects.filter(user=request.user)
    return render(request, 'appointments/my_addons.html', {'addon_orders': addon_orders})


@login_required
def upcoming_appointments(request):
    appointments = Appointment.objects.filter(
        patient=request.user,
        status__in=['Pending', 'Confirmed']
    )
    return render(request, 'appointments/upcoming.html', {'appointments': appointments})


@login_required
def past_appointments(request):
    appointments = Appointment.objects.filter(
        patient=request.user,
        status__in=['Completed', 'Cancelled']
    )
    return render(request, 'appointments/past.html', {'appointments': appointments})


def ajax_locations(request):
    if request.method == 'POST':
        city_id = request.POST.get('p')
        hotels = Hotel.objects.filter(city_id=city_id)
        html = ''
        for h in hotels:
            html += f'<option value="{h.id}">{h.name} {h.address}</option>'
        return JsonResponse({'html': html})
    return JsonResponse({'html': ''})
