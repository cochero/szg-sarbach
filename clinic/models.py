from django.db import models
from django.utils.text import slugify
from core.models import UserProfile


class City(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Cities'
        ordering = ['name']

    def __str__(self):
        return self.name


class Department(models.Model):
    TYPE_CHOICES = [
        ('deps', 'Department'),
        ('symptoms', 'Symptoms'),
    ]
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    dept_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='deps')
    icon = models.ImageField(upload_to='departments/', blank=True, null=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Treatment(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='treatments')
    image = models.ImageField(upload_to='treatments/', blank=True, null=True)
    description = models.TextField(blank=True)
    short_description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    duration_days = models.IntegerField(default=1)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class TreatmentStep(models.Model):
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE, related_name='steps')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.treatment.name} - Step {self.order}"


class Doctor(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, null=True, blank=True, related_name='doctor_profile')
    name = models.CharField(max_length=255)
    login_username = models.CharField(max_length=100, unique=True)
    password_hash = models.CharField(max_length=255)
    image = models.ImageField(upload_to='doctors/', default='images/doctor.jpg', blank=True)
    qualification = models.CharField(max_length=500, blank=True)
    specialization = models.CharField(max_length=500, blank=True)
    contact_number = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='doctors')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Staff(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, null=True, blank=True, related_name='staff_profile')
    name = models.CharField(max_length=255)
    login_username = models.CharField(max_length=100, unique=True)
    password_hash = models.CharField(max_length=255)
    image = models.ImageField(upload_to='staff/', default='images/user.png', blank=True)
    role = models.CharField(max_length=100, blank=True)
    contact_number = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)

    class Meta:
        verbose_name_plural = 'Staff'

    def __str__(self):
        return self.name


class Hotel(models.Model):
    TYPE_CHOICES = [
        ('Hotel', 'Hotel'),
        ('Apartment', 'Apartment'),
    ]
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name='hotels')
    address = models.TextField(blank=True)
    hotel_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='Apartment')
    phone = models.CharField(max_length=50, blank=True)
    rates = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='hotels/', default='images/hotel.jpg', blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Gallery(models.Model):
    GALLERY_TYPE_CHOICES = [
        ('treatment', 'Treatment'),
        ('hotel', 'Hotel'),
        ('doctor', 'Doctor'),
        ('general', 'General'),
    ]
    gallery_type = models.CharField(max_length=20, choices=GALLERY_TYPE_CHOICES, default='general')
    related_id = models.IntegerField(default=0)
    image = models.ImageField(upload_to='gallery/')

    class Meta:
        verbose_name_plural = 'Galleries'

    def __str__(self):
        return f"{self.gallery_type} - {self.id}"


class Addon(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='addons/', blank=True, null=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    duration = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class AddonPrice(models.Model):
    addon = models.ForeignKey(Addon, on_delete=models.CASCADE, related_name='prices')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.addon.title} - {self.duration}"


class Package(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField(blank=True)
    short_description = models.TextField(blank=True)
    duration_days = models.IntegerField(default=1)
    image = models.ImageField(upload_to='packages/', default='images/pack.jpg', blank=True)
    addons = models.ManyToManyField(Addon, blank=True, related_name='packages')
    treatments = models.ManyToManyField(Treatment, blank=True, related_name='packages')
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class DietItem(models.Model):
    name_en = models.CharField(max_length=255)
    name_de = models.CharField(max_length=255, blank=True)
    name_local = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='diets/', default='images/diet.png', blank=True)

    def __str__(self):
        return self.name_en
