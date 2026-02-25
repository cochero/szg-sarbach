from django.contrib import admin
from .models import (City, Department, Treatment, TreatmentStep, Doctor, 
                     Staff, Hotel, Gallery, Addon, AddonPrice, Package, DietItem)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'dept_type', 'is_active']
    list_filter = ['dept_type', 'is_active']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'price', 'duration_days', 'is_featured', 'is_active']
    list_filter = ['department', 'is_featured', 'is_active']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(TreatmentStep)
class TreatmentStepAdmin(admin.ModelAdmin):
    list_display = ['treatment', 'title', 'order']


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialization', 'department', 'is_active']
    list_filter = ['department', 'is_active']


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'email']


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'hotel_type', 'is_active']
    list_filter = ['hotel_type', 'is_active']


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['gallery_type', 'related_id']
    list_filter = ['gallery_type']


@admin.register(Addon)
class AddonAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'duration', 'is_active']


@admin.register(AddonPrice)
class AddonPriceAdmin(admin.ModelAdmin):
    list_display = ['addon', 'price', 'duration']


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'duration_days', 'is_active']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(DietItem)
class DietItemAdmin(admin.ModelAdmin):
    list_display = ['name_en', 'name_de']
