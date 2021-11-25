from .models import Appointment, Client, ReceptionDay
from django.forms import ModelForm, TextInput, Select, DateTimeInput, EmailInput, SplitDateTimeWidget, DateInput, \
    TimeInput, SplitDateTimeField, SelectDateWidget
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker


class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointment_time', 'reception_day']

        widgets = {
            "appointment_time": TextInput(attrs={
                 'id': 'appointment_time',
                 'name': 'appointment_time',
                 'placeholder': 'HH:MM'
            }),
            "reception_day": Select(attrs={
                'id': 'reception_day',
                'name': 'reception_day',
                # 'placeholder': ''
            })


        }


class AppointmentFormChange(ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointment_time', 'date_last_change', 'status', 'client', 'reception_day']

        widgets = {
            "appointment_time": TextInput(attrs={
                 'id': 'appointment_time',
                 'name': 'appointment_time',
                 'placeholder': 'HH:MM'
            }),
            "date_last_change": DateInput(attrs={
                 'id': 'date_last_change',
                 'name': 'date_last_change',
                 'placeholder': ''
            }),
            "status": Select(attrs={
                'id': 'status',
                'name': 'status',
                # 'placeholder': ''
            }),
            "client": Select(attrs={
                'id': 'client',
                'name': 'client',
                # 'placeholder': ''
            }),
            "reception_day": Select(attrs={
                'id': 'reception_day',
                'name': 'reception_day',
                # 'placeholder': ''
            })


        }


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'surname', 'email', 'telephone']

        widgets = {
            "name": TextInput(attrs={
                'id': 'name',
                'name': 'name',
                'placeholder': 'Впишите имя'
            }),
            "surname": TextInput(attrs={
                'id': 'last_name',
                'name': 'surname',
                'placeholder': 'Впишите фамилию'
            }),
            "email": EmailInput(attrs={
                'placeholder': "example@gmail.com",
                'id': "email",
                'name': "email"
            }),
            "telephone": TextInput(attrs={
                'id': "telephone",
                'name': "telephone",
                'placeholder': "",
                'default': "+"
            })
        }


class ClientSearchForm(ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'telephone']

        widgets = {
            "email": EmailInput(attrs={
                'placeholder': "example@gmail.com",
                'id': "email",
                'name': "email"
            }),
            "telephone": TextInput(attrs={
                'id': "telephone",
                'name': "telephone",
                'placeholder': "",
                'default': "+"
            })
        }