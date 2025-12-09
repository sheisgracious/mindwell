# mindwell/urls.py
# Gracious Ogyiri Asare -  gpoa@bu.edu

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),    
    path('login/', auth_views.LoginView.as_view(template_name='mindwell/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('providers/', ProviderListView.as_view(), name='provider_list'),
    path('providers/<int:pk>/', ProviderDetailView.as_view(), name='provider_detail'),
    path('provider/register/', CreateProviderView.as_view(), name='provider_register'),
    path('provider/<int:pk>/dashboard/', ProviderDashboardView.as_view(), name='provider_dashboard'),
    path('provider/update/', UpdateProviderView.as_view(), name='provider_update'),
    path('patient/<int:pk>/dashboard/', PatientDashboardView.as_view(), name='patient_dashboard'),
    path('patient/update/', UpdatePatientView.as_view(), name='patient_update'),
    path('provider/availability/', ManageAvailabilityView.as_view(), name='manage_availability'),
    path('provider/availability/<int:pk>/delete/', DeleteAvailabilityView.as_view(), name='delete_availability'),
    path('patient/register/', CreatePatientView.as_view(), name='patient_register'),
    path('therapyplan/create/<int:provider_pk>/', CreateTherapyPlanView.as_view(), name='therapyplan_create'),
    path('session/create/<int:plan_pk>/', CreateSessionView.as_view(), name='session_create'),
    path('session/<int:pk>/update/', UpdateSessionView.as_view(), name='session_update'),
    # path('therapyplan/<int:plan_pk>/add-note/', AddPatientNoteView.as_view(), name='add_patient_note'), -stretch
    path('therapyplan/<int:plan_pk>/send-message/', SendMessageView.as_view(), name='send_message'),
    path('messages/', ViewMessagesView.as_view(), name='view_messages'),

]