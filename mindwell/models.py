# mindwell/models.py
from django.db import models

# Create your models here.
class HealthProvider(models.Model):
    '''Model representing the health providers registered'''
    
    # data fields
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    email = models.TextField(blank=True)
    occupation = models.TextField(blank=True)
    address = models.TextField(blank=True)
    specialization = models.TextField(blank=True)
    experience_years = models.IntegerField(default=0)
    languages = models.TextField(blank=True)
    profile_img = models.ImageField(blank=True, null=True)
    bio = models.TextField(blank=True)
    verified = models.BooleanField(default=False)
    join_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name} is a {self.occupation} and specializes in {self.specialization}"

class Patient(models.Model):
    '''Model representing the patients registered'''
    
    # data fields
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    email = models.TextField(blank=True)
    dob = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True)
    emergency_contact_name = models.TextField(blank=True)
    emergency_contact_phone = models.TextField(blank=True)
    # profile_img = models.ImageField(blank=True, null=True)
    insurance_provider = models.TextField(blank=True)
    insurance_id = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"This is patient {self.first_name} {self.last_name}"

class Availability(models.Model):
    '''Model for the provider availability schedules'''
    
    # data fields
    health_provider = models.ForeignKey(HealthProvider, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10, choices=[
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.health_provider.first_name} is avaialble {self.day_of_week} {self.start_time}-{self.end_time}"
    

class PlanType(models.Model):
    '''Model for the different therapy plan types offered'''
    
    # data fields
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    base_cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class TherapyPlan(models.Model):
    '''Model representing the therapy plans assigned to patients'''
    
    # data fields
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    health_provider = models.ForeignKey(HealthProvider, on_delete=models.CASCADE)
    plan_type = models.ForeignKey(PlanType, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ])
    start_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.patient} is on {self.plan_type.name} with {self.health_provider}"

class Session(models.Model):
    '''Model representing therapy sessions'''
    
    # data fields
    therapy_plan = models.ForeignKey(TherapyPlan, on_delete=models.CASCADE)
    session_date = models.DateField()
    session_time = models.TimeField()
    duration = models.IntegerField(default=60)
    status = models.CharField(max_length=20, choices=[
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no-show', 'No-Show'),
    ])
    session_type = models.CharField(max_length=20, choices=[
        ('message', 'Message'),
        ('audio', 'Audio Chat'),
        ('video', 'Video Chat'),
    ])
    notes = models.TextField(blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=[
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
    ])
    follow_up_required = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Session {self.id} is for {self.therapy_plan.patient} on {self.session_date}"
