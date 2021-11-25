from django.contrib import admin
from .models import Doctor, Client, Appointment, Administrator, Status, ReceptionDay, AppHasAdmin


class AppHasAdminAdmin(admin.ModelAdmin):
    list_display = ('id', 'administrator', 'appointment', 'responsibility')
    list_display_links = ('administrator', 'appointment')
    search_fields = ('administrator', 'appointment')
    list_filter = ('administrator', 'appointment')


class ReceptionDayAdmin(admin.ModelAdmin):
    list_display = ('id', 'doctor', 'date', 'start_time', 'end_time', 'additional_info')
    list_display_links = ('doctor', 'date')
    search_fields = ('doctor', 'date')
    list_filter = ('doctor', 'date')


class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_display_links = ('name', )


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'reception_day', 'appointment_time', 'status', 'date_last_change')
    list_display_links = ('reception_day', 'appointment_time', 'status')
    search_fields = ('client', 'status')
    list_filter = ('reception_day', 'status', 'client')


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'email', 'telephone')
    list_display_links = ('name', 'surname')
    search_fields = ('name', 'surname')
    list_filter = ('name', 'surname')


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'email', 'telephone')
    list_display_links = ('name', 'surname')
    search_fields = ('name', 'surname')
    list_filter = ('name', 'surname')


class AdministratorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'email', 'telephone')
    list_display_links = ('name', 'surname')
    search_fields = ('name', 'surname')
    list_filter = ('name', 'surname')


admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Administrator, AdministratorAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(ReceptionDay, ReceptionDayAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(AppHasAdmin, AppHasAdminAdmin)

