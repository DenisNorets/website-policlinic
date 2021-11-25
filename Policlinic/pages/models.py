from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.db import models
import re


def phone_number(value):
    if not re.match(r'^[\+]{1}[\d]+$', value):
        raise ValidationError('Enter correct phone number')


class Doctor(models.Model):
    name = models.CharField(max_length=15, verbose_name='Имя доктора')
    surname = models.CharField(max_length=15, verbose_name='Фамилия доктора')
    email = models.EmailField(max_length=25, verbose_name='Email доктора', validators=[EmailValidator])
    telephone = models.CharField(max_length=20, verbose_name='Номер телефона доктора', validators=[phone_number])

    def __str__(self):
        return f'{self.name} {self.surname}'

    def get_absolute_url(self):
        return f'/database/{self.id}'

    class Meta:
        verbose_name = 'Доктор'
        verbose_name_plural = 'Доктора'
        ordering = ['name', 'surname']


class Client(models.Model):
    name = models.CharField(max_length=15, verbose_name='Имя клиента')
    surname = models.CharField(max_length=15, verbose_name='Фамилия клиента')
    email = models.EmailField(max_length=25, verbose_name='Email клиента', validators=[EmailValidator])
    telephone = models.CharField(max_length=20, default='+', verbose_name='Номер телефона клиента', validators=[phone_number])

    def __str__(self):
        return f'{self.name} {self.surname}'

    def get_absolute_url(self):
        return f'/database/{self.id}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['name', 'surname']


class Appointment(models.Model):

    appointment_time = models.TimeField(verbose_name='Время записи')
    date_last_change = models.DateField(verbose_name='Время последнего изменения')
    reception_day = models.ForeignKey('ReceptionDay', on_delete=models.PROTECT, verbose_name='День приема')
    status = models.ForeignKey('Status', on_delete=models.PROTECT, verbose_name='Статус записи')
    client = models.ForeignKey('Client', on_delete=models.PROTECT, verbose_name='Клиент')

    def __str__(self):
        return f'{self.client}, {self.reception_day} на {self.appointment_time}'

    def get_absolute_url(self):
        return f'/database/{self.id}'

    class Meta:
        verbose_name = 'Запись на прием'
        verbose_name_plural = 'Записи на прием'
        ordering = ['reception_day', 'appointment_time', 'client']


class AppHasAdmin(models.Model):

    responsibility = models.CharField(max_length=200, verbose_name='Ответственность за')
    administrator = models.ForeignKey('Administrator', on_delete=models.PROTECT, verbose_name='Администратор')
    appointment = models.ForeignKey('Appointment', on_delete=models.PROTECT, verbose_name='Запись на прием')

    def __str__(self):
        return f'Администратор - {self.administrator}, запись - {self.appointment}'

    def get_absolute_url(self):
        return f'/database/{self.id}'

    class Meta:
        verbose_name = 'Администратор к записи на прием'
        verbose_name_plural = 'Администраторы к записям на прием'
        ordering = ['administrator', 'appointment']


class Status(models.Model):
    name = models.CharField(max_length=25, verbose_name='Название статуса')
    description = models.CharField(max_length=180, verbose_name='Описание статуса', blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return f'/database/{self.id}'

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
        ordering = ['name']


class ReceptionDay(models.Model):
    date = models.DateField(verbose_name='Дата рабочего дня')
    start_time = models.TimeField(verbose_name='Начало дня')
    end_time = models.TimeField(verbose_name='Конец дня')
    additional_info = models.TextField(verbose_name='Доп. инфо')
    doctor = models.ForeignKey('Doctor', on_delete=models.PROTECT, verbose_name='Доктор')

    def __str__(self):
        return f'{self.date} ({self.start_time.strftime("%H:%M")} - {self.end_time.strftime("%H:%M")}) - {self.doctor}'

    def get_absolute_url(self):
        return f'/database/{self.id}'

    class Meta:
        verbose_name = 'День приема'
        verbose_name_plural = 'Дни приемов'
        ordering = ['date', 'doctor', 'start_time', 'end_time']


class Administrator(models.Model):
    name = models.CharField(max_length=15, verbose_name='Имя администратора')
    surname = models.CharField(max_length=15, verbose_name='Фамилия администратора')
    email = models.EmailField(max_length=25, verbose_name='Email администратора',
                              validators=[EmailValidator])
    telephone = models.CharField(max_length=20, default='+', verbose_name='Email администратора',
                                 validators=[phone_number])

    def __str__(self):
        return f'{self.name} {self.surname}'

    def get_absolute_url(self):
        return f'/database/{self.id}'

    class Meta:
        verbose_name = 'Администратор'
        verbose_name_plural = 'Администраторы'
        ordering = ['name', 'surname']