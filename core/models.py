from django.db import models
from django.contrib.auth.models import User


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=255, default='SZG Sarbach Health Centre')
    site_email = models.EmailField(default='help@sarbach.swiss')
    site_phone = models.CharField(max_length=50, default='+41 79 290 77 44')
    site_address = models.TextField(default='Gesundheit, Dorfstrasse 19, CH 3954, Leukerbad')
    logo = models.ImageField(upload_to='settings/', blank=True, null=True)
    favicon = models.ImageField(upload_to='settings/', blank=True, null=True)
    emr_nr = models.CharField(max_length=100, default='26054', blank=True)
    zsr_nr = models.CharField(max_length=100, default='B494360', blank=True)
    asca_id = models.CharField(max_length=100, default='106773', blank=True)
    egk_nr = models.CharField(max_length=100, default='42736', blank=True)
    gln_nr = models.CharField(max_length=100, default='7601002563383', blank=True)
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    about_title = models.CharField(max_length=255, default='SZG Sarbach Gesundheitszentrum', blank=True)
    about_content = models.TextField(blank=True, default='')
    about_image = models.ImageField(upload_to='settings/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.site_name


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('superadmin', 'Super Admin'),
        ('doctor', 'Doctor'),
        ('frontdesk', 'Front Desk'),
        ('patient', 'Patient'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient')
    phone = models.CharField(max_length=50, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', default='images/user.png', blank=True)
    gender = models.CharField(max_length=10, blank=True, choices=[('Male', 'Male'), ('Female', 'Female')])
    age = models.IntegerField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    street = models.CharField(max_length=255, blank=True)
    street_number = models.CharField(max_length=50, blank=True)
    plz = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    basic_insurance = models.CharField(max_length=255, blank=True)
    complementary_insurance = models.CharField(max_length=255, blank=True)
    signature = models.TextField(blank=True)
    registration_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.get_role_display()})"


class Banner(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='banners/')
    description = models.TextField(blank=True)
    link = models.CharField(max_length=500, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class ContactSubmission(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    subject = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"
