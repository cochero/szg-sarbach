from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models import Count, Sum
from core.models import Banner, ContactSubmission, UserProfile, SiteSettings
from clinic.models import (Department, Treatment, TreatmentStep, Doctor, Staff,
                           Hotel, City, Gallery, Addon, AddonPrice, Package, DietItem)
from appointments.models import Appointment, Examination, AddonOrder, PatientRecord, AppointmentDiet
from shop.models import Medicine, Order, OrderItem
from blog_app.models import BlogPost
import hashlib


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('admin_login_page')
        if not (request.user.is_superuser or 
                (hasattr(request.user, 'profile') and 
                 request.user.profile.role in ['superadmin', 'frontdesk'])):
            return redirect('admin_login_page')
        return view_func(request, *args, **kwargs)
    return wrapper


def doctor_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('doctor_login_page')
        if not (hasattr(request.user, 'profile') and request.user.profile.role == 'doctor'):
            return redirect('doctor_login_page')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def dashboard(request):
    context = {
        'doctor_count': Doctor.objects.count(),
        'patient_count': UserProfile.objects.filter(role='patient').count(),
        'appointment_count': Appointment.objects.count(),
        'order_count': Order.objects.count(),
        'recent_appointments': Appointment.objects.select_related('patient', 'doctor', 'treatment')[:10],
        'recent_orders': Order.objects.select_related('user')[:5],
    }
    return render(request, 'admin_panel/dashboard.html', context)


@admin_required
def doctor_list(request):
    doctors = Doctor.objects.select_related('department', 'city').all()
    departments = Department.objects.filter(dept_type='deps')
    cities = City.objects.all()
    return render(request, 'admin_panel/doctor_list.html', {
        'doctors': doctors, 'departments': departments, 'cities': cities,
    })


@admin_required
def doctor_submit(request):
    if request.method == 'POST':
        doc_img = request.FILES.get('doc_img')
        user = User.objects.create_user(
            username=request.POST['doc_login'],
            password=request.POST['doc_pass'],
            first_name=request.POST['name'],
            email=request.POST.get('email', ''),
        )
        profile = UserProfile.objects.create(user=user, role='doctor')
        Doctor.objects.create(
            user_profile=profile, name=request.POST['name'],
            login_username=request.POST['doc_login'],
            password_hash=hashlib.md5(request.POST['doc_pass'].encode()).hexdigest(),
            image=doc_img or 'images/doctor.jpg',
            qualification=request.POST.get('qualification', ''),
            specialization=request.POST.get('specialization', ''),
            contact_number=request.POST.get('contact_number', ''),
            email=request.POST.get('email', ''),
            address=request.POST.get('address', ''),
            department_id=request.POST.get('department') or None,
            city_id=request.POST.get('city') or None,
        )
        messages.success(request, 'Doctor added successfully')
    return redirect('admin_doctor_list')


@admin_required
def doctor_update(request):
    if request.method == 'POST':
        doctor = get_object_or_404(Doctor, pk=request.POST['d_id'])
        doctor.name = request.POST['name']
        doctor.login_username = request.POST['doc_login']
        doctor.qualification = request.POST.get('qualification', '')
        doctor.specialization = request.POST.get('specialization', '')
        doctor.contact_number = request.POST.get('contact_number', '')
        doctor.email = request.POST.get('email', '')
        doctor.address = request.POST.get('address', '')
        doctor.department_id = request.POST.get('department') or None
        doctor.city_id = request.POST.get('city') or None
        if request.FILES.get('doc_img'):
            doctor.image = request.FILES['doc_img']
        doctor.save()
        messages.success(request, 'Doctor updated successfully')
    return redirect('admin_doctor_list')


@admin_required
def department_list(request, dtype='deps'):
    departments = Department.objects.filter(dept_type=dtype)
    return render(request, 'admin_panel/department_list.html', {'departments': departments, 'dtype': dtype})


@admin_required
def department_submit(request):
    if request.method == 'POST':
        Department.objects.create(
            name=request.POST['department'],
            slug=slugify(request.POST['department']),
            dept_type=request.POST.get('dtype', 'deps'),
        )
        messages.success(request, 'Department added successfully')
    return redirect('admin_department_list', dtype=request.POST.get('dtype', 'deps'))


@admin_required
def department_update(request):
    if request.method == 'POST':
        dept = get_object_or_404(Department, pk=request.POST['departmentid'])
        dept.name = request.POST['department']
        dept.slug = slugify(request.POST['department'])
        dept.save()
        messages.success(request, 'Department updated successfully')
    return redirect('admin_department_list', dtype=request.POST.get('dtype', 'deps'))


@admin_required
def department_delete(request):
    if request.method == 'POST':
        Department.objects.filter(pk=request.POST['id']).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@admin_required
def department_toggle(request):
    if request.method == 'POST':
        dept = get_object_or_404(Department, pk=request.POST['id'])
        dept.is_active = request.POST.get('st') != 'Disable'
        dept.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@admin_required
def treatment_list(request):
    treatments = Treatment.objects.select_related('department').all()
    departments = Department.objects.filter(dept_type='deps')
    return render(request, 'admin_panel/treatment_list.html', {'treatments': treatments, 'departments': departments})


@admin_required
def treatment_submit(request):
    if request.method == 'POST':
        t_img = request.FILES.get('t_img')
        Treatment.objects.create(
            name=request.POST['t_name'], slug=slugify(request.POST['t_name']),
            department_id=request.POST.get('t_dep') or None, image=t_img,
            description=request.POST.get('t_desc', ''),
            short_description=request.POST.get('t_sdesc', ''),
            price=request.POST.get('t_price', 0) or 0,
            duration_days=request.POST.get('t_days', 1) or 1,
        )
        messages.success(request, 'Treatment added successfully')
    return redirect('admin_treatment_list')


@admin_required
def treatment_update(request):
    if request.method == 'POST':
        treat = get_object_or_404(Treatment, pk=request.POST['t_id'])
        treat.name = request.POST['t_name']
        treat.slug = slugify(request.POST['t_name'])
        treat.department_id = request.POST.get('t_dep') or None
        treat.description = request.POST.get('t_desc', '')
        treat.price = request.POST.get('t_price', 0) or 0
        treat.duration_days = request.POST.get('t_days', 1) or 1
        if request.FILES.get('t_img'):
            treat.image = request.FILES['t_img']
        treat.save()
        messages.success(request, 'Treatment updated successfully')
    return redirect('admin_treatment_list')


@admin_required
def treatment_toggle(request):
    if request.method == 'POST':
        treat = get_object_or_404(Treatment, pk=request.POST['id'])
        treat.is_active = request.POST.get('st') != 'Disable'
        treat.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@admin_required
def treatment_delete(request):
    if request.method == 'POST':
        Treatment.objects.filter(pk=request.POST['id']).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@admin_required
def patient_list(request):
    patients = UserProfile.objects.filter(role='patient').select_related('user')
    return render(request, 'admin_panel/patient_list.html', {'patients': patients})


@admin_required
def patient_register(request):
    if request.method == 'POST':
        from datetime import datetime, date
        pimg = request.FILES.get('pimg')
        dob_str = request.POST.get('dob', '')
        dob = None
        age = 0
        if dob_str:
            try:
                dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
                age = (date.today() - dob).days // 365
            except ValueError:
                pass
        email = request.POST.get('email', '')
        username = email or f"patient_{User.objects.count()}"
        user = User.objects.create_user(
            username=username, email=email,
            first_name=request.POST.get('name', ''),
            last_name=request.POST.get('givenname', ''),
        )
        UserProfile.objects.create(
            user=user, role='patient', phone=request.POST.get('mobile', ''),
            gender=request.POST.get('gender', ''), age=age, dob=dob,
            street=request.POST.get('street', ''),
            street_number=request.POST.get('streetnumber', ''),
            plz=request.POST.get('plz', ''), city=request.POST.get('city', ''),
            state=request.POST.get('state', ''),
            basic_insurance=request.POST.get('binsurance', ''),
            complementary_insurance=request.POST.get('cinsurance', ''),
            profile_image=pimg or 'images/user.png',
        )
        messages.success(request, 'Patient registered successfully')
    return redirect('admin_patient_list')


@admin_required
def patient_update(request):
    if request.method == 'POST':
        from datetime import datetime, date
        profile = get_object_or_404(UserProfile, pk=request.POST['p_id'])
        profile.user.first_name = request.POST.get('name', '')
        profile.user.last_name = request.POST.get('givenname', '')
        profile.user.email = request.POST.get('email', '')
        profile.user.save()
        profile.phone = request.POST.get('mobile', '')
        profile.gender = request.POST.get('gender', '')
        dob_str = request.POST.get('dob', '')
        if dob_str:
            try:
                profile.dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
                profile.age = (date.today() - profile.dob).days // 365
            except ValueError:
                pass
        profile.street = request.POST.get('street', '')
        profile.street_number = request.POST.get('streetnumber', '')
        profile.plz = request.POST.get('plz', '')
        profile.city = request.POST.get('city', '')
        profile.state = request.POST.get('state', '')
        profile.basic_insurance = request.POST.get('binsurance', '')
        profile.complementary_insurance = request.POST.get('cinsurance', '')
        if request.FILES.get('pimg'):
            profile.profile_image = request.FILES['pimg']
        profile.save()
        messages.success(request, 'Patient updated successfully')
    return redirect('admin_patient_list')


@admin_required
def patient_history(request, pk):
    profile = get_object_or_404(UserProfile, pk=pk)
    appointments = Appointment.objects.filter(patient=profile.user)
    examinations = Examination.objects.filter(patient=profile.user)
    return render(request, 'admin_panel/patient_history.html', {
        'patient_profile': profile, 'appointments': appointments, 'examinations': examinations,
    })


@admin_required
def appointment_list(request):
    appointments = Appointment.objects.select_related('patient', 'doctor', 'department', 'treatment', 'city').all()
    departments = Department.objects.filter(dept_type='deps')
    doctors = Doctor.objects.filter(is_active=True)
    cities = City.objects.all()
    patients = UserProfile.objects.filter(role='patient').select_related('user')
    return render(request, 'admin_panel/appointment_list.html', {
        'appointments': appointments, 'departments': departments,
        'doctors': doctors, 'cities': cities, 'patients': patients,
    })


@admin_required
def appointment_create(request):
    if request.method == 'POST':
        try:
            app_date_str = request.POST.get('app_date', '')
            try:
                parts = app_date_str.split('/')
                app_date = f"{parts[2]}-{parts[1]}-{parts[0]}"
            except (IndexError, ValueError):
                app_date = app_date_str
            Appointment.objects.create(
                patient_id=request.POST['app_pat'],
                appointment_date=app_date,
                appointment_time=request.POST.get('app_time') or None,
                amount=request.POST.get('app_amt', 0) or 0,
                city_id=request.POST.get('app_city') or None,
                location_id=request.POST.get('app_location') or None,
                appointment_type=request.POST.get('app_type', 'Walkin'),
                description=request.POST.get('app_desc', ''),
                department_id=request.POST.get('app_dept') or None,
                treatment_id=request.POST.get('app_treat') or None,
                payment_status=request.POST.get('app_payment', 'Pending'),
                payment_remarks=request.POST.get('pay_remarks', ''),
                status=request.POST.get('app_status', 'Pending'),
                created_by=request.POST.get('app_created', 'Admin'),
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False})


@admin_required
def appointment_update(request):
    if request.method == 'POST':
        try:
            appt = get_object_or_404(Appointment, pk=request.POST['app_id'])
            appt.doctor_id = request.POST.get('app_doctor') or None
            appt.appointment_time = request.POST.get('app_time') or None
            appt.payment_status = request.POST.get('app_payment', 'Pending')
            appt.status = request.POST.get('app_status', 'Pending')
            appt.appointment_date = request.POST.get('app_date', appt.appointment_date)
            appt.amount = request.POST.get('app_amt', 0) or 0
            appt.city_id = request.POST.get('app_city') or None
            appt.location_id = request.POST.get('app_location') or None
            appt.description = request.POST.get('app_desc', '')
            appt.payment_remarks = request.POST.get('pay_remarks', '')
            appt.department_id = request.POST.get('app_dept') or None
            appt.treatment_id = request.POST.get('app_treat') or None
            appt.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False})


@admin_required
def examination_list(request):
    examinations = Examination.objects.select_related('patient', 'doctor').all()
    return render(request, 'admin_panel/examination_list.html', {'examinations': examinations})


@admin_required
def examination_submit(request):
    if request.method == 'POST':
        Examination.objects.create(
            appointment_id=request.POST.get('appt_id') or None,
            patient_id=request.POST['patient'],
            doctor_id=request.POST.get('doctor') or None,
            blood_pressure=request.POST.get('blood_pressure', ''),
            pulse=request.POST.get('pulse', ''),
            temperature=request.POST.get('temperature', ''),
            weight=request.POST.get('weight', ''),
            height=request.POST.get('height', ''),
            diagnosis=request.POST.get('diagnosis', ''),
            treatments_prescribed=request.POST.get('treatments', ''),
            remark=request.POST.get('remark', ''),
        )
        messages.success(request, 'Examination recorded successfully')
    return redirect('admin_examination_list')


@admin_required
def hotel_list(request):
    hotels = Hotel.objects.select_related('city').all()
    cities = City.objects.all()
    return render(request, 'admin_panel/hotel_list.html', {'hotels': hotels, 'cities': cities})


@admin_required
def hotel_submit(request):
    if request.method == 'POST':
        h_img = request.FILES.get('h_img')
        Hotel.objects.create(
            name=request.POST['h_name'], city_id=request.POST.get('h_city') or None,
            address=request.POST.get('h_add', ''), hotel_type=request.POST.get('h_type', 'Apartment'),
            phone=request.POST.get('h_phn', ''), rates=request.POST.get('h_rates', ''),
            description=request.POST.get('h_des', ''), image=h_img or 'images/hotel.jpg',
        )
        messages.success(request, 'Hotel/Apartment added successfully')
    return redirect('admin_hotel_list')


@admin_required
def hotel_update(request):
    if request.method == 'POST':
        hotel = get_object_or_404(Hotel, pk=request.POST['h_id'])
        hotel.name = request.POST['h_name']
        hotel.city_id = request.POST.get('h_city') or None
        hotel.address = request.POST.get('h_add', '')
        hotel.hotel_type = request.POST.get('h_type', 'Apartment')
        hotel.phone = request.POST.get('h_phn', '')
        hotel.rates = request.POST.get('h_rates', '')
        hotel.description = request.POST.get('h_des', '')
        if request.FILES.get('h_img'):
            hotel.image = request.FILES['h_img']
        hotel.save()
        messages.success(request, 'Hotel/Apartment updated successfully')
    return redirect('admin_hotel_list')


@admin_required
def hotel_delete(request):
    if request.method == 'POST':
        Hotel.objects.filter(pk=request.POST['id']).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@admin_required
def hotel_toggle(request):
    if request.method == 'POST':
        hotel = get_object_or_404(Hotel, pk=request.POST['id'])
        hotel.is_active = request.POST.get('st') != 'Disable'
        hotel.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@admin_required
def city_list(request):
    cities = City.objects.all()
    return render(request, 'admin_panel/city_list.html', {'cities': cities})


@admin_required
def city_submit(request):
    if request.method == 'POST':
        City.objects.create(name=request.POST['city_name'])
        messages.success(request, 'City added successfully')
    return redirect('admin_city_list')


@admin_required
def banner_list(request):
    banners = Banner.objects.all()
    return render(request, 'admin_panel/banner_list.html', {'banners': banners})


@admin_required
def banner_submit(request):
    if request.method == 'POST':
        bann_img = request.FILES.get('bann_img')
        Banner.objects.create(
            title=request.POST['bann_title'], image=bann_img,
            description=request.POST.get('bann_desc', ''),
            link=request.POST.get('bann_link', ''),
        )
        messages.success(request, 'Banner added successfully')
    return redirect('admin_banner_list')


@admin_required
def banner_update(request):
    if request.method == 'POST':
        banner = get_object_or_404(Banner, pk=request.POST['bann_id'])
        banner.title = request.POST['bann_title']
        banner.description = request.POST.get('bann_desc', '')
        banner.link = request.POST.get('bann_link', '')
        if request.FILES.get('bann_img'):
            banner.image = request.FILES['bann_img']
        banner.save()
        messages.success(request, 'Banner updated successfully')
    return redirect('admin_banner_list')


@admin_required
def banner_delete(request):
    if request.method == 'POST':
        Banner.objects.filter(pk=request.POST['id']).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@admin_required
def banner_toggle(request):
    if request.method == 'POST':
        banner = get_object_or_404(Banner, pk=request.POST['id'])
        banner.is_active = request.POST.get('st') != 'Disable'
        banner.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@admin_required
def package_list_admin(request):
    packages = Package.objects.all()
    treatments = Treatment.objects.filter(is_active=True)
    addons = Addon.objects.filter(is_active=True)
    return render(request, 'admin_panel/package_list.html', {
        'packages': packages, 'treatments': treatments, 'addons': addons,
    })


@admin_required
def package_submit(request):
    if request.method == 'POST':
        pack_img = request.FILES.get('pack_img')
        pack = Package.objects.create(
            title=request.POST['pack_title'], slug=slugify(request.POST['pack_title']),
            price=request.POST.get('pack_price', 0) or 0,
            description=request.POST.get('pack_desc', ''),
            short_description=request.POST.get('pack_sdesc', ''),
            duration_days=request.POST.get('pack_days', 1) or 1,
            image=pack_img or 'images/pack.jpg',
        )
        if request.POST.getlist('pack_trts'):
            pack.treatments.set(request.POST.getlist('pack_trts'))
        if request.POST.getlist('pack_addons'):
            pack.addons.set(request.POST.getlist('pack_addons'))
        messages.success(request, 'Package added successfully')
    return redirect('admin_package_list')


@admin_required
def package_update(request):
    if request.method == 'POST':
        pack = get_object_or_404(Package, pk=request.POST['pack_id'])
        pack.title = request.POST['pack_title']
        pack.slug = slugify(request.POST['pack_title'])
        pack.price = request.POST.get('pack_price', 0) or 0
        pack.description = request.POST.get('pack_desc', '')
        pack.short_description = request.POST.get('pack_sdesc', '')
        pack.duration_days = request.POST.get('pack_days', 1) or 1
        if request.FILES.get('pack_img'):
            pack.image = request.FILES['pack_img']
        pack.save()
        if request.POST.getlist('pack_trts'):
            pack.treatments.set(request.POST.getlist('pack_trts'))
        if request.POST.getlist('pack_addons'):
            pack.addons.set(request.POST.getlist('pack_addons'))
        messages.success(request, 'Package updated successfully')
    return redirect('admin_package_list')


@admin_required
def package_delete(request):
    if request.method == 'POST':
        Package.objects.filter(pk=request.POST['id']).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@admin_required
def package_toggle(request):
    if request.method == 'POST':
        pack = get_object_or_404(Package, pk=request.POST['id'])
        pack.is_active = request.POST.get('st') != 'Disable'
        pack.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@admin_required
def addon_list_admin(request):
    addons = Addon.objects.all()
    return render(request, 'admin_panel/addon_list.html', {'addons': addons})


@admin_required
def addon_submit(request):
    if request.method == 'POST':
        ad_img = request.FILES.get('ad_img')
        Addon.objects.create(
            title=request.POST['ad_title'], image=ad_img,
            description=request.POST.get('ad_desc', ''),
            price=request.POST.get('ad_price', 0) or 0,
            duration=request.POST.get('ad_duration', ''),
        )
        messages.success(request, 'Addon added successfully')
    return redirect('admin_addon_list')


@admin_required
def addon_update(request):
    if request.method == 'POST':
        addon = get_object_or_404(Addon, pk=request.POST['ad_id'])
        addon.title = request.POST['ad_title']
        addon.description = request.POST.get('ad_desc', '')
        addon.price = request.POST.get('ad_price', 0) or 0
        addon.duration = request.POST.get('ad_duration', '')
        if request.FILES.get('ad_img'):
            addon.image = request.FILES['ad_img']
        addon.save()
        messages.success(request, 'Addon updated successfully')
    return redirect('admin_addon_list')


@admin_required
def addon_delete(request):
    if request.method == 'POST':
        Addon.objects.filter(pk=request.POST['id']).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@admin_required
def addon_toggle(request):
    if request.method == 'POST':
        addon = get_object_or_404(Addon, pk=request.POST['id'])
        addon.is_active = request.POST.get('st') != 'Disable'
        addon.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@admin_required
def blog_list_admin(request):
    posts = BlogPost.objects.all()
    return render(request, 'admin_panel/blog_list.html', {'posts': posts})


@admin_required
def blog_submit(request):
    if request.method == 'POST':
        b_img = request.FILES.get('b_img')
        BlogPost.objects.create(
            title=request.POST['b_tittle'], slug=slugify(request.POST['b_tittle']),
            date=request.POST.get('b_date', ''), description=request.POST.get('b_des', ''),
            author=request.POST.get('b_auth', ''), image=b_img,
            post_type=request.POST.get('b_type', 'Blog'),
        )
        messages.success(request, 'Post added successfully')
    return redirect('admin_blog_list')


@admin_required
def blog_update(request):
    if request.method == 'POST':
        post = get_object_or_404(BlogPost, pk=request.POST['b_id'])
        post.title = request.POST['b_tittle']
        post.slug = slugify(request.POST['b_tittle'])
        post.date = request.POST.get('b_date', post.date)
        post.description = request.POST.get('b_des', '')
        post.author = request.POST.get('b_auth', '')
        post.post_type = request.POST.get('b_type', 'Blog')
        if request.FILES.get('b_img'):
            post.image = request.FILES['b_img']
        post.save()
        messages.success(request, 'Post updated successfully')
    return redirect('admin_blog_list')


@admin_required
def blog_delete(request):
    if request.method == 'POST':
        BlogPost.objects.filter(pk=request.POST['id']).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@admin_required
def blog_toggle(request):
    if request.method == 'POST':
        post = get_object_or_404(BlogPost, pk=request.POST['id'])
        post.is_active = request.POST.get('st') != 'Disable'
        post.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@admin_required
def order_list(request):
    orders = Order.objects.select_related('user').all()
    return render(request, 'admin_panel/order_list.html', {'orders': orders})


@admin_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    items = order.items.all()
    return render(request, 'admin_panel/order_detail.html', {'order': order, 'items': items})


@admin_required
def addon_order_list(request):
    addon_orders = AddonOrder.objects.select_related('user', 'city').all()
    return render(request, 'admin_panel/addon_order_list.html', {'addon_orders': addon_orders})


@admin_required
def package_order_list(request):
    package_orders = AddonOrder.objects.filter(order_type='Package').select_related('user', 'city')
    return render(request, 'admin_panel/package_order_list.html', {'package_orders': package_orders})


@admin_required
def enquiry_list(request):
    enquiries = ContactSubmission.objects.all()
    return render(request, 'admin_panel/enquiry_list.html', {'enquiries': enquiries})


@admin_required
def diet_list(request):
    diets = DietItem.objects.all()
    return render(request, 'admin_panel/diet_list.html', {'diets': diets})


@admin_required
def diet_submit(request):
    if request.method == 'POST':
        item_img = request.FILES.get('item_img')
        DietItem.objects.create(
            name_en=request.POST['item_name1'],
            name_de=request.POST.get('item_name2', ''),
            name_local=request.POST.get('item_name3', ''),
            description=request.POST.get('item_desc', ''),
            image=item_img or 'images/diet.png',
        )
        messages.success(request, 'Diet item added successfully')
    return redirect('admin_diet_list')


@admin_required
def medicine_list(request):
    medicines = Medicine.objects.select_related('department').all()
    departments = Department.objects.filter(dept_type='deps')
    return render(request, 'admin_panel/medicine_list.html', {'medicines': medicines, 'departments': departments})


@admin_required
def medicine_submit(request):
    if request.method == 'POST':
        m_img = request.FILES.get('m_img')
        Medicine.objects.create(
            name=request.POST['m_name'],
            department_id=request.POST.get('m_dep') or None,
            price=request.POST.get('m_price', 0) or 0,
            quantity=request.POST.get('m_qty', ''),
            image=m_img,
            description=request.POST.get('m_desc', ''),
        )
        messages.success(request, 'Medicine added successfully')
    return redirect('admin_medicine_list')


@admin_required
def medicine_update(request):
    if request.method == 'POST':
        med = get_object_or_404(Medicine, pk=request.POST['m_id'])
        med.name = request.POST['m_name']
        med.department_id = request.POST.get('m_dep') or None
        med.price = request.POST.get('m_price', 0) or 0
        med.quantity = request.POST.get('m_qty', '')
        med.description = request.POST.get('m_desc', '')
        if request.FILES.get('m_img'):
            med.image = request.FILES['m_img']
        med.save()
        messages.success(request, 'Medicine updated successfully')
    return redirect('admin_medicine_list')


@admin_required
def medicine_delete(request):
    if request.method == 'POST':
        Medicine.objects.filter(pk=request.POST['id']).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@admin_required
def settings_page(request):
    settings_obj, _ = SiteSettings.objects.get_or_create(pk=1)
    if request.method == 'POST':
        settings_obj.site_name = request.POST.get('site_name', settings_obj.site_name)
        settings_obj.site_email = request.POST.get('site_email', settings_obj.site_email)
        settings_obj.site_phone = request.POST.get('site_phone', settings_obj.site_phone)
        settings_obj.site_address = request.POST.get('site_address', settings_obj.site_address)
        if request.FILES.get('logo'):
            settings_obj.logo = request.FILES['logo']
        if request.FILES.get('favicon'):
            settings_obj.favicon = request.FILES['favicon']
        settings_obj.emr_nr = request.POST.get('emr_nr', settings_obj.emr_nr)
        settings_obj.zsr_nr = request.POST.get('zsr_nr', settings_obj.zsr_nr)
        settings_obj.asca_id = request.POST.get('asca_id', settings_obj.asca_id)
        settings_obj.egk_nr = request.POST.get('egk_nr', settings_obj.egk_nr)
        settings_obj.gln_nr = request.POST.get('gln_nr', settings_obj.gln_nr)
        settings_obj.facebook_url = request.POST.get('facebook_url', settings_obj.facebook_url)
        settings_obj.twitter_url = request.POST.get('twitter_url', settings_obj.twitter_url)
        settings_obj.linkedin_url = request.POST.get('linkedin_url', settings_obj.linkedin_url)
        settings_obj.instagram_url = request.POST.get('instagram_url', settings_obj.instagram_url)
        settings_obj.about_title = request.POST.get('about_title', settings_obj.about_title)
        settings_obj.about_content = request.POST.get('about_content', settings_obj.about_content)
        if request.FILES.get('about_image'):
            settings_obj.about_image = request.FILES['about_image']
        settings_obj.save()
        messages.success(request, 'Settings updated successfully')
    return render(request, 'admin_panel/settings.html', {'settings': settings_obj})


@admin_required
def staff_list(request):
    staff = Staff.objects.all()
    return render(request, 'admin_panel/staff_list.html', {'staff': staff})


@admin_required
def staff_submit(request):
    if request.method == 'POST':
        staff_img = request.FILES.get('staff_img')
        user = User.objects.create_user(
            username=request.POST['staff_login'],
            password=request.POST['staff_pass'],
            first_name=request.POST['name'],
            email=request.POST.get('email', ''),
        )
        profile = UserProfile.objects.create(user=user, role='frontdesk')
        Staff.objects.create(
            user_profile=profile, name=request.POST['name'],
            login_username=request.POST['staff_login'],
            password_hash=hashlib.md5(request.POST['staff_pass'].encode()).hexdigest(),
            image=staff_img or 'images/user.png',
            role=request.POST.get('role', ''),
            contact_number=request.POST.get('contact_number', ''),
            email=request.POST.get('email', ''),
        )
        messages.success(request, 'Staff added successfully')
    return redirect('admin_staff_list')


@admin_required
def ajax_patient_search(request):
    if request.method == 'POST':
        query = request.POST.get('p', '')
        patients = UserProfile.objects.filter(role='patient').select_related('user').filter(
            user__first_name__icontains=query
        ) | UserProfile.objects.filter(role='patient').select_related('user').filter(
            user__last_name__icontains=query
        )
        results = [{'id': p.user.id, 'name': p.user.get_full_name(), 'phone': p.phone, 'email': p.user.email} for p in patients[:20]]
        return JsonResponse({'patients': results})
    return JsonResponse({'patients': []})


@admin_required
def gallery_upload(request):
    if request.method == 'POST':
        gl_img = request.FILES.get('gl_img')
        if gl_img:
            Gallery.objects.create(
                gallery_type=request.POST.get('gl_type', 'general'),
                related_id=request.POST.get('gl_id2', 0),
                image=gl_img,
            )
            return JsonResponse({'success': True, 'message': 'Uploaded'})
    return JsonResponse({'success': False})


@admin_required
def gallery_delete(request):
    if request.method == 'POST':
        Gallery.objects.filter(pk=request.POST['id']).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@doctor_required
def doctor_dashboard(request):
    try:
        doctor = Doctor.objects.get(user_profile=request.user.profile)
        appointments = Appointment.objects.filter(doctor=doctor).select_related('patient', 'treatment')
    except Doctor.DoesNotExist:
        appointments = Appointment.objects.none()
        doctor = None
    return render(request, 'admin_panel/doctor_dashboard.html', {
        'doctor': doctor, 'appointments': appointments,
    })


@doctor_required
def doctor_appointments(request):
    try:
        doctor = Doctor.objects.get(user_profile=request.user.profile)
        appointments = Appointment.objects.filter(doctor=doctor).select_related('patient', 'treatment')
    except Doctor.DoesNotExist:
        appointments = Appointment.objects.none()
    return render(request, 'admin_panel/doctor_appointments.html', {'appointments': appointments})
