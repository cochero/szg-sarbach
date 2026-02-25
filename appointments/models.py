from django.db import models
from django.contrib.auth.models import User
from clinic.models import City, Hotel, Department, Treatment, Doctor, DietItem


class PatientRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='patient_records')
    family_name = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255)
    present_complaints = models.TextField(blank=True)
    history_present_complaints = models.TextField(blank=True)
    past_illness = models.TextField(blank=True)
    history_past_illness = models.TextField(blank=True)
    dob = models.DateField(null=True, blank=True)
    family_history = models.TextField(blank=True)
    stress_level = models.CharField(max_length=50, blank=True)
    habits = models.TextField(blank=True)
    sleep = models.CharField(max_length=100, blank=True)
    allergies = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.family_name}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    TYPE_CHOICES = [
        ('Walkin', 'Walk-in'),
        ('Telephonic', 'Telephonic'),
        ('Online', 'Online'),
    ]
    PAYMENT_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Insurance', 'Insurance'),
    ]
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, blank=True)
    appointment_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='Walkin')
    description = models.TextField(blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    treatment = models.ForeignKey(Treatment, on_delete=models.SET_NULL, null=True, blank=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='Pending')
    payment_remarks = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['-appointment_date', '-appointment_time']

    def __str__(self):
        return f"Appt #{self.id} - {self.patient.get_full_name()} on {self.appointment_date}"


class Examination(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True, blank=True, related_name='examinations')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='examinations')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    exam_date = models.DateField(auto_now_add=True)
    blood_pressure = models.CharField(max_length=50, blank=True)
    pulse = models.CharField(max_length=50, blank=True)
    temperature = models.CharField(max_length=50, blank=True)
    weight = models.CharField(max_length=50, blank=True)
    height = models.CharField(max_length=50, blank=True)
    respiratory_rate = models.CharField(max_length=50, blank=True)
    spo2 = models.CharField(max_length=50, blank=True)
    general_appearance = models.TextField(blank=True)
    skin = models.TextField(blank=True)
    tongue = models.TextField(blank=True)
    nails = models.TextField(blank=True)
    eyes = models.TextField(blank=True)
    appetite = models.TextField(blank=True)
    digestion = models.TextField(blank=True)
    bowel = models.TextField(blank=True)
    urination = models.TextField(blank=True)
    sleep_quality = models.TextField(blank=True)
    perspiration = models.TextField(blank=True)
    prakriti = models.TextField(blank=True)
    diagnosis = models.TextField(blank=True)
    treatments_prescribed = models.TextField(blank=True)
    remark = models.TextField(blank=True)

    class Meta:
        ordering = ['-exam_date']

    def __str__(self):
        return f"Exam for {self.patient.get_full_name()} on {self.exam_date}"


class AppointmentDiet(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='diet_plans')
    diet_item = models.ForeignKey(DietItem, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Diet for Appt #{self.appointment.id}"


class AddonOrder(models.Model):
    TYPE_CHOICES = [
        ('Addon', 'Addon'),
        ('Package', 'Package'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addon_orders')
    addon_id = models.IntegerField()
    order_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='Addon')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    order_date = models.DateField(auto_now_add=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    accommodation = models.CharField(max_length=255, blank=True)
    accommodation_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    accommodation_days = models.IntegerField(default=0, null=True, blank=True)
    status = models.CharField(max_length=20, default='Pending')
    payment_status = models.CharField(max_length=20, default='Pending')

    class Meta:
        ordering = ['-order_date']

    def __str__(self):
        return f"Addon Order #{self.id} by {self.user.get_full_name()}"


class PackageSchedule(models.Model):
    addon_order = models.ForeignKey(AddonOrder, on_delete=models.CASCADE, related_name='schedules')
    schedule_date = models.DateField()
    activity = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['schedule_date']

    def __str__(self):
        return f"Schedule for Order #{self.addon_order.id}"
