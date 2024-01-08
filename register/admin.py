from django.contrib import admin
from .models import Appointment, Option, Stylist, Address, Times, Blocks, WorkSchedule, Portfolio
# Register your models here.
class WorkScheduleAdmin(admin.ModelAdmin):
    list_display = ('stylist', 'day_of_work', 'is_work', )
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'client_name','appointment_beg_date','stylist','client_phone','proof', )
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Option)
admin.site.register(Stylist)
admin.site.register(Address)
admin.site.register(Times)
admin.site.register(WorkSchedule, WorkScheduleAdmin)
admin.site.register(Blocks)
admin.site.register(Portfolio)