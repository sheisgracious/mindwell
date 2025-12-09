# mindwell/views.py
# Gracious Ogyiri Asare - gpoa@bu.edu
# Views for MindWell app

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.contrib import messages
from .models import *
from .forms import *

# Create your views here.

class MethodLoginRequiredMixin(LoginRequiredMixin):
    '''Method to require login and provide helper methods'''
    
    def get_login_url(self):
        '''Return login URL'''
        return reverse('login')
    
    def get_provider(self):
        '''Get provider profile '''
        return HealthProvider.objects.get(user=self.request.user)
    
    def is_provider(self):
        '''Check if provider'''
        return HealthProvider.objects.filter(user=self.request.user).exists()
    def get_patient(self):
        '''Get patient profile '''
        return Patient.objects.get(user=self.request.user)
    
    def is_patient(self):
        '''Check if is a patient'''
        return Patient.objects.filter(user=self.request.user).exists()

class HomePageView(TemplateView):
    '''Display home page'''
    template_name = 'mindwell/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_provider'] = HealthProvider.objects.filter(user=self.request.user).exists()
            context['is_patient'] = Patient.objects.filter(user=self.request.user).exists()
            
            if context['is_patient']:
                context['patient'] = Patient.objects.get(user=self.request.user)
            if context['is_provider']:
                context['provider'] = HealthProvider.objects.get(user=self.request.user)
        return context

class ProviderListView(ListView):
    '''Display all providers'''
    model = HealthProvider
    template_name = 'mindwell/provider_list.html'
    context_object_name = 'providers'
    
    def get_queryset(self):
        '''Return only verified providers, with optional filtering'''
        queryset = HealthProvider.objects.filter()
        
        # search parameters
        specialization = self.request.GET.get('specialization', '')
        language = self.request.GET.get('language', '')
        search = self.request.GET.get('search', '')
        
        if specialization:
            queryset = queryset.filter(specialization__icontains=specialization)
        
        if language:
            queryset = queryset.filter(languages__icontains=language)
            
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(specialization__icontains=search) |
                Q(bio__icontains=search)
            )
        
        return queryset.order_by('last_name', 'first_name')
    
    def get_context_data(self, **kwargs):
        '''add search parameters to context'''
        context = super().get_context_data(**kwargs)
        context['specialization'] = self.request.GET.get('specialization', '')
        context['language'] = self.request.GET.get('language', '')
        context['search'] = self.request.GET.get('search', '')
        
        if self.request.user.is_authenticated:
            context['is_patient'] = Patient.objects.filter(user=self.request.user).exists()
            context['is_provider'] = HealthProvider.objects.filter(user=self.request.user).exists()
            if context['is_patient']:
                context['patient'] = Patient.objects.get(user=self.request.user)
            if context['is_provider']:
                context['provider'] = HealthProvider.objects.get(user=self.request.user)
        
        return context

class ProviderDetailView(DetailView):
    '''Display one provider profile'''
    model = HealthProvider
    template_name = 'mindwell/provider_detail.html'
    context_object_name = 'provider'
    
    def get_context_data(self, **kwargs):
        '''add availability and plan types to context'''
        context = super().get_context_data(**kwargs)
        provider = self.object
        
        context['availability_by_day'] = provider.get_availability_by_day()
        context['plan_types'] = provider.get_supported_plan_types()
        
        if self.request.user.is_authenticated:
            context['is_patient'] = Patient.objects.filter(user=self.request.user).exists()
            context['is_provider'] = HealthProvider.objects.filter(user=self.request.user).exists()
            
            if context['is_patient']:
                context['patient'] = Patient.objects.get(user=self.request.user)
            if context['is_provider']:
                context['provider_user'] = HealthProvider.objects.get(user=self.request.user)
        
        return context

class CreateProviderView(CreateView):
    '''Create a new provider profile with user registration'''
    form_class = CreateProviderForm
    template_name = 'mindwell/create_provider_form.html'
    
    def get_context_data(self, **kwargs):
        '''Add user form to context'''
        context = super().get_context_data(**kwargs)
        if 'user_form' not in context:
            context['user_form'] = UserCreationForm()
        return context
    
    def form_valid(self, form):
        '''Process user and provider creation'''
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(self.request, user)
            form.instance.user = user
            form.instance.verified = True
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

class CreatePatientView(CreateView):
    '''Create a new patient profile with user registration'''
    form_class = CreatePatientForm
    template_name = 'mindwell/create_patient_form.html'
    
    def get_context_data(self, **kwargs):
        '''add user form to context'''
        context = super().get_context_data(**kwargs)
        if 'user_form' not in context:
            context['user_form'] = UserCreationForm()
        return context
    
    def form_valid(self, form):
        '''Process user and patient creation'''
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(self.request, user)
            form.instance.user = user
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

class PatientDashboardView(MethodLoginRequiredMixin, DetailView):
    '''Display patient dashboard'''
    model = Patient
    template_name = 'mindwell/patient_dashboard.html'
    context_object_name = 'patient'
    
    def dispatch(self, request, *args, **kwargs):
        logged_in_patient = Patient.objects.filter(user=request.user).first()
        if not logged_in_patient:
            return redirect("home")

        requested_patient = self.get_object()
        if logged_in_patient.pk != requested_patient.pk:
            return redirect("patient_dashboard", pk=logged_in_patient.pk)

        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        '''Add therapy plans and sessions to context'''
        context = super().get_context_data(**kwargs)
        patient = self.object
        
        context['active_plans'] = patient.get_active_plans()
        context['all_plans'] = TherapyPlan.objects.filter(patient=patient).order_by('-created_at')
        context['upcoming_sessions'] = patient.get_upcoming_sessions()
        context['is_patient'] = True
        
        from datetime import date
        context['past_sessions'] = Session.objects.filter(
            therapy_plan__patient=patient,
            status__in=['completed', 'cancelled', 'no-show']
        ).order_by('-session_date', '-session_time')[:10]
        
        # Get unread messages
        context['unread_messages'] = Message.objects.filter(
            recipient=self.request.user,
            is_read=False
        ).count()
        
        return context

class ProviderDashboardView(MethodLoginRequiredMixin, DetailView):
    '''Display provider dashboard'''
    model = HealthProvider
    template_name = 'mindwell/provider_dashboard.html'
    context_object_name = 'provider'
    
    def dispatch(self, request, *args, **kwargs):
        logged_in_provider = HealthProvider.objects.filter(user=request.user).first()
        if not logged_in_provider:
            return redirect("home")

        requested_provider = self.get_object()
        if logged_in_provider.pk != requested_provider.pk:
            return redirect("provider_dashboard", pk=logged_in_provider.pk)

        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        '''Add therapy plans and sessions to context'''
        context = super().get_context_data(**kwargs)
        provider = self.object
        
        context['active_plans'] = provider.get_active_plans()
        context['upcoming_sessions'] = provider.get_upcoming_sessions()
        context['is_provider'] = True
        
        from datetime import date
        context['today_sessions'] = Session.objects.filter(
            therapy_plan__health_provider=provider,
            session_date=date.today(),
            status='scheduled'
        ).order_by('session_time')
        
        # Get unread messages
        context['unread_messages'] = Message.objects.filter(
            recipient=self.request.user,
            is_read=False
        ).count()
        
        return context

class CreateTherapyPlanView(MethodLoginRequiredMixin, CreateView):
    '''Create a new therapy plan'''
    form_class = CreateTherapyPlanForm
    template_name = 'mindwell/create_therapyplan_form.html'
    
    def get_form_kwargs(self):
        '''Pass provider to form'''
        kwargs = super().get_form_kwargs()
        provider_pk = self.kwargs.get('provider_pk')
        if provider_pk:
            kwargs['provider'] = HealthProvider.objects.get(pk=provider_pk)
        return kwargs
    
    def get_context_data(self, **kwargs):
        '''override context'''
        context = super().get_context_data(**kwargs)
        provider_pk = self.kwargs.get('provider_pk')
        if provider_pk:
            context['provider'] = HealthProvider.objects.get(pk=provider_pk)
        context['is_patient'] = True
        context['patient'] = self.get_patient()
        return context
    
    def form_valid(self, form):
        '''Set values'''
        patient = self.get_patient()
        provider_pk = self.kwargs.get('provider_pk')
        provider = HealthProvider.objects.get(pk=provider_pk)
        
        form.instance.patient = patient
        form.instance.health_provider = provider
        form.instance.status = 'active'
        form.instance.cost = form.instance.plan_type.base_cost
        
        messages.success(self.request, f'Therapy plan created with Dr. {provider.last_name}!')
        return super().form_valid(form)
    
    def get_success_url(self):
        '''Redirect to dashboard'''
        patient = self.get_patient()
        return reverse('patient_dashboard', kwargs={'pk': patient.pk})

class CreateSessionView(MethodLoginRequiredMixin, CreateView):
    '''Create a new session'''
    form_class = CreateSessionForm
    template_name = 'mindwell/create_session_form.html'
    
    def get_form_kwargs(self):
        '''Pass therapy plan to form'''
        kwargs = super().get_form_kwargs()
        plan_pk = self.kwargs.get('plan_pk')
        if plan_pk:
            kwargs['therapy_plan'] = TherapyPlan.objects.get(pk=plan_pk)
        return kwargs
    
    def get_context_data(self, **kwargs):
        '''Add therapy plan and availability to context'''
        context = super().get_context_data(**kwargs)
        plan_pk = self.kwargs.get('plan_pk')
        if plan_pk:
            therapy_plan = TherapyPlan.objects.get(pk=plan_pk)
            context['therapy_plan'] = therapy_plan
            context['availability_by_day'] = therapy_plan.health_provider.get_availability_by_day()
        context['is_patient'] = True
        context['patient'] = self.get_patient()
        return context
    
    def form_valid(self, form):
        '''Set therapy plans'''
        plan_pk = self.kwargs.get('plan_pk')
        therapy_plan = TherapyPlan.objects.get(pk=plan_pk)
        
        form.instance.therapy_plan = therapy_plan
        form.instance.status = 'scheduled'
        form.instance.payment_status = 'unpaid'
        
        messages.success(self.request, 'Session booked successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        '''Redirect to dashboard'''
        patient = self.get_patient()
        return reverse('patient_dashboard', kwargs={'pk': patient.pk})

class UpdateSessionView(MethodLoginRequiredMixin, UpdateView):
    '''Update session details'''
    model = Session
    form_class = UpdateSessionForm
    template_name = 'mindwell/update_session_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        provider = HealthProvider.objects.filter(user=request.user).first()
        if not provider:
            return redirect("home")

        session = self.get_object()
        if session.therapy_plan.health_provider_id != provider.id:
            return redirect("provider_dashboard", pk=provider.pk)

        return super().dispatch(request, *args, **kwargs)
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        '''Add provider to context'''
        context = super().get_context_data(**kwargs)
        context['provider'] = self.get_provider()
        context['is_provider'] = True
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Session updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        '''Redirect to provider dashboard'''
        provider = self.get_provider()
        return reverse('provider_dashboard', kwargs={'pk': provider.pk})

class UpdateProviderView(MethodLoginRequiredMixin, UpdateView):
    '''Update provider profile'''
    model = HealthProvider
    form_class = UpdateProviderForm
    template_name = 'mindwell/update_provider_form.html'
    
    def get_object(self):
        '''Get provider profile of logged in user'''
        return self.get_provider()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_provider'] = True
        context['provider'] = self.get_provider()
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        '''Redirect to provider dashboard'''
        provider = self.get_provider()
        return reverse('provider_dashboard', kwargs={'pk': provider.pk})

class UpdatePatientView(MethodLoginRequiredMixin, UpdateView):
    '''Update patient profile'''
    model = Patient
    form_class = UpdatePatientForm
    template_name = 'mindwell/update_patient_form.html'
    
    def get_object(self):
        '''Get patient profile of logged in user'''
        return self.get_patient()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_patient'] = True
        context['patient'] = self.get_patient()
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        '''Redirect to patient dashboard'''
        patient = self.get_patient()
        return reverse('patient_dashboard', kwargs={'pk': patient.pk})

class ManageAvailabilityView(MethodLoginRequiredMixin, TemplateView):
    '''Manage provider availability'''
    template_name = 'mindwell/manage_availability.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.provider = HealthProvider.objects.filter(user=request.user).first()
        if not self.provider:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['provider'] = self.provider
        context['availability_by_day'] = self.provider.get_availability_by_day()
        context['form'] = AvailabilityForm()
        context['is_provider'] = True
        return context
    
    def post(self, request, *args, **kwargs):
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.health_provider = self.provider
            availability.save()
            messages.success(request, "Availability added successfully!")
        else:
            messages.error(request, "Please correct the form errors.")

        return redirect("provider_dashboard", pk=self.provider.pk)


class DeleteAvailabilityView(MethodLoginRequiredMixin, DeleteView):
    model = Availability

    def dispatch(self, request, *args, **kwargs):
        provider = HealthProvider.objects.filter(user=request.user).first()
        if not provider:
            return redirect("home")

        availability = self.get_object()
        if availability.health_provider_id != provider.id:
            return redirect("provider_dashboard", pk=provider.pk)

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        provider = HealthProvider.objects.get(user=self.request.user)
        return reverse("provider_dashboard", args=[provider.pk])

# class AddPatientNoteView(MethodLoginRequiredMixin, CreateView):
#     '''Add a note for patient progress- stretch'''
#     model = PatientNote
#     form_class = PatientNoteForm
#     template_name = 'mindwell/add_patient_note.html'
    
#     def dispatch(self, request, *args, **kwargs):
#         '''Check if user is the provider for this therapy plan'''
#         plan_pk = self.kwargs.get('plan_pk')
#         therapy_plan = get_object_or_404(TherapyPlan, pk=plan_pk)
        
#         
#         provider = HealthProvider.objects.get(user=request.user)
#
#         self.therapy_plan = therapy_plan
#         return super().dispatch(request, *args, **kwargs)
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['therapy_plan'] = self.therapy_plan
#         context['existing_notes'] = self.therapy_plan.patient_notes.all()[:10]
#         context['is_provider'] = True
#         context['provider'] = self.get_provider()
#         return context
    
#     def form_valid(self, form):
#         form.instance.therapy_plan = self.therapy_plan
#         form.instance.provider = self.get_provider()
#         messages.success(self.request, 'Note added successfully!')
#         return super().form_valid(form)
    
#     def get_success_url(self):
#         provider = self.get_provider()
#         return reverse('provider_dashboard', kwargs={'pk': provider.pk})

class SendMessageView(MethodLoginRequiredMixin, CreateView):
    '''Send a message to a patient or provider'''
    model = Message
    form_class = MessageForm
    template_name = 'mindwell/send_message.html'
    
    def dispatch(self, request, *args, **kwargs):
        '''Check if user has permission to send message'''
        plan_pk = self.kwargs.get('plan_pk')
        self.therapy_plan = get_object_or_404(TherapyPlan, pk=plan_pk)
        
        # Check if user is either the provider or patient in this therapy plan
        is_provider = HealthProvider.objects.filter(
            user=request.user, 
            id=self.therapy_plan.health_provider.id
        ).exists()
        is_patient = Patient.objects.filter(
            user=request.user,
            id=self.therapy_plan.patient.id
        ).exists()
        
        if not (is_provider or is_patient):
            return HttpResponseForbidden("You can only message within your therapy plans.")
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['therapy_plan'] = self.therapy_plan
        
        if self.request.user == self.therapy_plan.patient.user:
            context['is_patient'] = True
            context['patient'] = self.therapy_plan.patient
        else:
            context['is_provider'] = True
            context['provider'] = self.therapy_plan.health_provider
        
        context['message_list'] = self.therapy_plan.messages.all().order_by('created_at')
        return context
    
    
    def form_valid(self, form):
        form.instance.therapy_plan = self.therapy_plan
        form.instance.sender = self.request.user
        
        # Set recipient
        if self.request.user == self.therapy_plan.patient.user:
            form.instance.recipient = self.therapy_plan.health_provider.user
        else:
            form.instance.recipient = self.therapy_plan.patient.user
        
        messages.success(self.request, 'Message sent successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('send_message', kwargs={'plan_pk': self.therapy_plan.pk})

class ViewMessagesView(MethodLoginRequiredMixin, ListView):
    model = Message
    template_name = "mindwell/view_messages.html"
    context_object_name = "user_messages"  # IMPORTANT: don't use "messages"

    def get_queryset(self):
        return Message.objects.filter(
            Q(sender=self.request.user) | Q(recipient=self.request.user)
        ).select_related(
            "therapy_plan__patient",
            "therapy_plan__health_provider",
            "therapy_plan__plan_type",
        ).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # mark unread as read
        Message.objects.filter(recipient=self.request.user, is_read=False).update(is_read=True)

        # role context
        context["is_provider"] = HealthProvider.objects.filter(user=self.request.user).exists()
        context["is_patient"] = Patient.objects.filter(user=self.request.user).exists()
        if context["is_provider"]:
            context["provider"] = HealthProvider.objects.get(user=self.request.user)
        if context["is_patient"]:
            context["patient"] = Patient.objects.get(user=self.request.user)

        # build one "thread" per therapy plan (latest msg wins because queryset is -created_at)
        threads_by_plan = {}
        for m in context["user_messages"]:
            if m.therapy_plan_id not in threads_by_plan:
                threads_by_plan[m.therapy_plan_id] = m
        context["threads"] = list(threads_by_plan.values())

        return context

