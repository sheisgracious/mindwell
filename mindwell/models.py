# mindwell/models.py
# Gracious Ogyiri Asare - gpoa@bu.edu

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date, time, timedelta

class HealthProvider(models.Model):
    '''Model representing the health providers registered'''
    
    # data fields
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    email = models.TextField(blank=True)
    gender = models.CharField(max_length=10, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], blank=True)
    occupation = models.TextField(blank=True)
    address = models.TextField(blank=True)
    specialization = models.TextField(blank=True)
    experience_years = models.IntegerField(default=0)
    languages = models.TextField(blank=True)
    profile_img = models.ImageField(blank=True, null=True)
    bio = models.TextField(blank=True)
    verified = models.BooleanField(default=True)
    join_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        '''String representation of the model object'''
        return f"Dr. {self.first_name} {self.last_name}"
    
    def get_absolute_url(self):
        '''Return URL to access this provider'''
        return reverse('provider_dashboard', kwargs={'pk': self.pk})
    
    def get_active_plans(self):
        '''Return active therapy plans for this provider'''
        return TherapyPlan.objects.filter(health_provider=self, status='active')
    
    def get_upcoming_sessions(self):
        '''Return upcoming sessions for this provider'''
        return Session.objects.filter(
            therapy_plan__health_provider=self,
            session_date__gte=date.today(),
            status='scheduled'
        ).order_by('session_date', 'session_time')
    
    def get_availability_by_day(self): #to group the availability slots by days
        '''Return availability grouped by day of week'''
        days_order = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        availability = {}
        for day in days_order:
            slots = Availability.objects.filter(
                health_provider=self,
                day_of_week=day,
                is_available=True
            ).order_by('start_time')
            if slots.exists():
                availability[day] = slots
        return availability
    
    def get_supported_plan_types(self):
        '''Return plan types this provider supports'''
        return self.supported_plan_types.filter(is_active=True)

class Patient(models.Model):
    '''Model representing the patients registered'''
    
    # data fields
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    email = models.TextField(blank=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], blank=True)
    address = models.TextField(blank=True)
    emergency_contact_name = models.TextField(blank=True)
    emergency_contact_phone = models.TextField(blank=True)
    insurance_provider = models.TextField(blank=True)
    insurance_id = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now_add=True)
    therapy_description = models.TextField(blank=True)
    
    def __str__(self):
        '''String representation of the model object'''
        return f"{self.first_name} {self.last_name}"
    
    def get_absolute_url(self):
        '''Return URL to access this patient'''
        return reverse('patient_dashboard', kwargs={'pk': self.pk})
    
    def get_active_plans(self):
        '''Return active therapy plans for this patient'''
        return TherapyPlan.objects.filter(patient=self, status='active')
    
    def get_upcoming_sessions(self):
        '''Return upcoming sessions for this patient'''
        return Session.objects.filter(
            therapy_plan__patient=self,
            session_date__gte=date.today(),
            status='scheduled'
        ).order_by('session_date', 'session_time')

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
    
    class Meta:
        verbose_name_plural = 'Availabilities'
        ordering = ['day_of_week', 'start_time']
    
    def __str__(self):
        '''String representation of the model object'''
        return f"{self.health_provider.first_name} - {self.day_of_week} {self.start_time}-{self.end_time}"
    
    def is_slot_booked(self, target_date):
        '''Check if this availability slot is already booked on a specific date'''
        return Session.objects.filter(
            therapy_plan__health_provider=self.health_provider,
            session_date=target_date,
            session_time__gte=self.start_time,
            session_time__lt=self.end_time,
            status='scheduled'
        ).exists()

class PlanType(models.Model):
    '''Model for the different therapy plan types offered'''
    
    # data fields
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    base_cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    providers = models.ManyToManyField(HealthProvider, related_name='supported_plan_types', blank=True)
    
    def __str__(self):
        '''String representation of the model object'''
        return f'{self.name} - ${self.base_cost}' 

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
        '''String representation of the model object'''
        return f"{self.patient} - {self.plan_type.name} with {self.health_provider}"

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
        '''String representation of the model object'''
        return f"Session {self.id} - {self.therapy_plan.patient} on {self.session_date}"

class Message(models.Model):
    '''Model for messages between providers and patients'''
    
    therapy_plan = models.ForeignKey(TherapyPlan, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.sender.username} to {self.recipient.username} about {self.message}"