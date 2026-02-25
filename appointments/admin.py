from django.contrib import admin
from .models import PatientRecord, Appointment, Examination, AppointmentDiet, AddonOrder, PackageSchedule


@admin.register(PatientRecord)
class PatientRecordAdmin(admin.ModelAdmin):
    list_display = ['name', 'family_name', 'dob', 'created_at']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'appointment_date', 'status', 'payment_status']
    list_filter = ['status', 'payment_status', 'appointment_type']


@admin.register(Examination)
class ExaminationAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'exam_date', 'diagnosis']


@admin.register(AppointmentDiet)
class AppointmentDietAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'diet_item']


@admin.register(AddonOrder)
class AddonOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'order_type', 'order_date', 'total', 'status']
    list_filter = ['order_type', 'status']


@admin.register(PackageSchedule)
class PackageScheduleAdmin(admin.ModelAdmin):
    list_display = ['addon_order', 'schedule_date']
