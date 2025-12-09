# mindwell/forms.py
# Gracious Ogyiri Asare - gpoa@bu.edu

from django import forms
from .models import HealthProvider, Patient, TherapyPlan, Session, Availability, Message
from datetime import date

class CreateProviderForm(forms.ModelForm):
    '''A form to create a new provider profile'''
    class Meta:
        model = HealthProvider
        fields = ['first_name', 'last_name', 'email', 'gender', 'occupation', 
                 'specialization', 'experience_years', 'languages', 
                 'address', 'profile_img', 'bio']

class CreatePatientForm(forms.ModelForm):
    '''A form to create a new patient profile'''
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'email', 'dob', 'gender', 'address',
                 'emergency_contact_name', 'emergency_contact_phone',
                 'insurance_provider', 'insurance_id', 'therapy_description']

class UpdateProviderForm(forms.ModelForm):
    '''A form to handle an update to a provider profile'''
    class Meta:
        model = HealthProvider
        fields = ['first_name', 'last_name', 'email', 'bio', 'profile_img', 'languages']

class UpdatePatientForm(forms.ModelForm):
    '''A form to handle an update to a patient profile'''
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'address', 'emergency_contact_name', 
                 'emergency_contact_phone', 'insurance_provider', 'insurance_id']

class CreateTherapyPlanForm(forms.ModelForm):
    '''A form to create a therapy plan - cost is set by provider's plan type'''
    class Meta:
        model = TherapyPlan
        fields = ['plan_type', 'start_date', 'notes']
    
    def __init__(self, *args, **kwargs):
        provider = kwargs.pop('provider', None)
        super().__init__(*args, **kwargs)
        
        # Only show plan types supported by this provider
        if provider:
            self.fields['plan_type'].queryset = provider.get_supported_plan_types()
        
        # Set minimum date to today
        self.fields['start_date'].widget = forms.DateInput(attrs={'type': 'date', 'min': date.today()})

class CreateSessionForm(forms.ModelForm):
    '''A form to book a session based on provider availability'''
    class Meta:
        model = Session
        fields = ['session_date', 'session_time', 'duration', 'session_type']
        widgets = {
            'session_date': forms.DateInput(attrs={'type': 'date'}),
            'session_time': forms.TimeInput(attrs={'type': 'time'}),
        }
    
    def __init__(self, *args, **kwargs):
        therapy_plan = kwargs.pop('therapy_plan', None)
        super().__init__(*args, **kwargs)
        
        # Set minimum date to today
        self.fields['session_date'].widget.attrs['min'] = date.today()
        
        # Add help text about availability
        if therapy_plan:
            provider = therapy_plan.health_provider
            self.fields['session_date'].help_text = f"Check Dr. {provider.last_name}'s availability below"
            self.fields['session_time'].help_text = "Choose a time within available hours"

class UpdateSessionForm(forms.ModelForm):
    '''A form to update session details (for providers)'''
    class Meta:
        model = Session
        fields = ['status', 'notes', 'payment_status', 'follow_up_required']

class AvailabilityForm(forms.ModelForm):
    '''A form for providers to set their availability'''
    class Meta:
        model = Availability
        fields = ['day_of_week', 'start_time', 'end_time', 'is_available']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

# class PatientNoteForm(forms.ModelForm):
#     '''A form for providers to add notes about patient progress'''
#     class Meta:
#         model = PatientNote
#         fields = ['note']
#         widgets = {
#             'note': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Add progress notes...'})
#         }

class MessageForm(forms.ModelForm):
    '''A form for sending messages between providers and patients'''
    class Meta:
        model = Message
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 6})
        }