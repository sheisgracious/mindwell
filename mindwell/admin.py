from django.contrib import admin
from mindwell.models import *

# Register your models here.
admin.site.register(HealthProvider)
admin.site.register(Patient)
admin.site.register(TherapyPlan)    
admin.site.register(Session)
admin.site.register(Availability)
admin.site.register(PlanType)
admin.site.register(Message)
