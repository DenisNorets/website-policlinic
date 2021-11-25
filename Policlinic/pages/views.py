from datetime import datetime, date
import re

from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone

from .models import Doctor, Appointment, Client, Status, ReceptionDay
from .forms import AppointmentForm, ClientForm, ClientSearchForm, AppointmentFormChange
from django.views.decorators.csrf import csrf_exempt


def main(request, name=''):
    context = {
        "title_msg": "Районная поликлиника",
    }
    if 'name' in request.GET.keys():
        context['name'] = request.GET['name']
    if name != '':
        context['name'] = name
    if request.session.get('call', '') == 1:
        context['confirmation_message'] = request.session.get('confirm_message', '')
        request.session['call'] = 0
    return render(request, 'Policlinic.html', context)


def shedule(request):
    context = {
        "title": "Расписание медперсонала",
    }
    test_view = Doctor.objects.order_by('name')
    context['news'] = test_view
    if request.method == 'GET':
        with connection.cursor() as cursor:
            query_app = f"SELECT First_name, Last_name, Date, Start_time_of_day, End_time_of_day, reception_day_id, d.doctor_id FROM doctor as d left join reception_day as r on d.doctor_id=r.doctor_id order by d.doctor_id, date"
            cursor.execute(query_app)
            context['doctors'] = cursor.fetchall()
            if context['doctors'] != 'None':
                print(context['doctors'])
                with connection.cursor() as cursor:
                    query_app = f"select distinct r.doctor_id, d.First_name, d.Last_name from doctor d inner join reception_day r on d.doctor_id = r.doctor_id;"
                    cursor.execute(query_app)
                    context['ids'] = cursor.fetchall()
                    print(context['ids'])
                return render(request, 'Shedule.html', context)


def contacts(request):
    context = {
        "title": "Контакты",
    }
    return render(request, 'Contacts.html', context)


def test(request):
    my_context = {
        "title": "Районная поликлиника",
    }
    return render(request, 'test.html', context=my_context)


def appointment_view(request, day_id=-1):
    print(day_id)
    client_form = ClientForm()
    app_form = AppointmentForm()
    context = {
        "title": "Запись на прием",
        "client_form": client_form,
        "app_form": app_form,
        "error": ""
    }
    if request.method == 'GET':
        if day_id != -1:
            print(day_id)
            day = ReceptionDay.objects.get(id=day_id)
            appointment_form = AppointmentForm(initial={'reception_day': day})
            context['app_form'] = appointment_form
            return render(request, 'Appointment.html', context)
        else:
            return render(request, 'Appointment.html', context)
    if request.method == 'POST':
        client_form = ClientForm(request.POST)
        app_form = AppointmentForm(request.POST)
        if app_form.is_valid() and client_form.is_valid():
            context['client_form'] = client_form
            context['app_form'] = app_form
            test_time = request.POST['appointment_time']
            if ':' in test_time[:2]:
                test_time_hour = int(test_time[:1])
                test_time_minute = int(test_time[2:])
            else:
                test_time_minute = int(test_time[3:])
                test_time_hour = int(test_time[:2])
            reception_day = ReceptionDay.objects.filter(id=request.POST['reception_day']).first()
            appointments = Appointment.objects.filter(reception_day_id=request.POST['reception_day'])
            start_time_hour = reception_day.start_time.hour
            start_time_minute = reception_day.start_time.minute
            end_time_hour = reception_day.end_time.hour
            end_time_minute = reception_day.end_time.minute
            if test_time_hour < start_time_hour:
                context['error'] = f"Введено неккоректное время приема \n Время начала приема: " \
                                   f"{reception_day.start_time.strftime('%H:%M')}"
                return render(request, 'Appointment.html', context)
            elif test_time_hour == start_time_hour and test_time_minute < start_time_minute:
                context['error'] = f"Введено неккоректное время приема \n Время начала приема: " \
                                   f"{reception_day.start_time.strftime('%H:%M')}"
                return render(request, 'Appointment.html', context)
            elif (test_time_hour - end_time_hour) >= 0:
                if test_time_minute >= end_time_minute:
                    context['error'] = f"Введено неккоректное время приема \nВремя окончания приема: " \
                                       f"{reception_day.end_time.strftime('%H:%M')}"
                    return render(request, 'Appointment.html', context)
                if abs(test_time_minute - end_time_minute) < 30:
                    context['error'] = f"Введено неккоректное время приема \nВремя окончания приема: " \
                                       f"{reception_day.end_time.strftime('%H:%M')} \nДлительность приема: 30 минут"
                    return render(request, 'Appointment.html', context)
            elif (end_time_hour - test_time_hour) == 1:
                if (60 - abs(test_time_minute - end_time_minute)) < 30:
                    context['error'] = f"Введено неккоректное время приема \n Время окончания приема: " \
                                       f"{reception_day.end_time.strftime('%H:%M')} \nДлительность приема: 30 минут"
                    return render(request, 'Appointment.html', context)
            #start_time_hour
            #start_time_minute
            #end_time_hour
            #end_time_minute
            all_time = []
            busy_time = []
            for appointment in appointments:
                minute = appointment.appointment_time.minute
                hour = appointment.appointment_time.hour
                if minute == 0:
                    tmp_str = str(hour) + ':' + '00'
                else:
                    tmp_str = str(hour) + ':' + str(minute)
                busy_time.append(tmp_str)
            for hour in range(start_time_hour, end_time_hour+1):
                if hour == start_time_hour:
                    if start_time_minute == 0:
                        tmp_str = str(hour) + ':' + '00'
                        all_time.append(tmp_str)
                        tmp_str = str(hour) + ':' + '30'
                        all_time.append(tmp_str)
                    elif start_time_minute == 30:
                        tmp_str = str(hour) + ':' + '30'
                        all_time.append(tmp_str)
                if hour != end_time_hour and hour != start_time_hour:
                    tmp_str = str(hour) + ':' + '00'
                    all_time.append(tmp_str)
                    tmp_str = str(hour) + ':' + '30'
                    all_time.append(tmp_str)
                elif end_time_minute == 30:
                    tmp_str = str(hour) + ':' + '00'
                    all_time.append(tmp_str)
            usage_times = ''
            iteration = 1
            print('-------------')
            print(busy_time)
            for one_time in all_time:
                print(one_time)
                print('-----')
                if one_time not in busy_time and iteration < 4:
                    if iteration == 1:
                        usage_times += f' {one_time}'
                    else:
                        usage_times += f', {one_time}'
                    iteration += 1

            for appointment in appointments:
                minute = appointment.appointment_time.minute
                hour = appointment.appointment_time.hour
                tmp_str = str(hour) + ':' + str(minute)
                if test_time_hour == hour:
                    if abs(minute-test_time_minute) < 30:
                        context['error'] = f'К сожалению, данное время уже занято, ближайшее свободное время ' \
                                           f'в выбранный день - {usage_times}'
                        return render(request, 'Appointment.html', context)
                elif abs(test_time_hour-hour) <= 1:
                    if abs(60 - abs(minute - test_time_minute)) < 30:
                        context['error'] = f'К сожалению, данное время уже занято, ближайшее свободное время ' \
                                           'в выбранный день - {usage_times}'
                        return render(request, 'Appointment.html', context)

            try_client = Client.objects.filter(email=request.POST['email'], telephone=request.POST['telephone']).first()
            if try_client is None:
                client = Client(name=request.POST['name'], surname=request.POST['surname'],
                                email=request.POST['email'], telephone=request.POST['telephone'])
                client.save()
                with connection.cursor() as cursor:
                    query_app = f"INSERT INTO  Client (First_name, Last_name, Client_telephone, Client_email) VALUES ('{request.POST['name']}','{request.POST['surname']}','{request.POST['telephone']}','{request.POST['email']}');"
                    cursor.execute(query_app)

            client = Client.objects.filter(email=request.POST['email'], telephone=request.POST['telephone']).first()
            status = Status.objects.get(name='Ожидается подтверждение')
            reception_day = ReceptionDay.objects.get(id=request.POST['reception_day'])
            reception_day_id = request.POST['reception_day']
            print(date.today())
            appointment = Appointment(appointment_time=request.POST['appointment_time'],
                                      date_last_change=date.today(),
                                      reception_day=reception_day,
                                      status=status, client=client)

            with connection.cursor() as cursor:
                query_app = f"SELECT Client_id FROM client WHERE Client_telephone = '{request.POST['telephone']}' AND Client_email = '{request.POST['email']}'"
                cursor.execute(query_app)
                result = cursor.fetchone()
                client_id = result[0]
            with connection.cursor() as cursor:
                query_app = f"SELECT Status_id from Appointment_status WHERE name = 'Ожидается подтверждение';"
                cursor.execute(query_app)
                result = cursor.fetchone()
                status_id = result[0]
            with connection.cursor() as cursor:
                query_app = f"INSERT INTO Appointment (Time_of_appointment, Reception_day_id, Status_id, CLient_id, Date_of_change) VALUES ('{request.POST['appointment_time']}', '{reception_day_id}', '{status_id}', '{client_id}', CURDATE());"
                result = cursor.execute(query_app)
                print(result)

            appointment.save()
            message = 'Запись на прием успешно оформлена.\nДля подтверждения введенной информации с вами позже ' \
                      'свяжется администратор системы'
            request.session['confirm_message'] = message
            request.session['call'] = 1
            return redirect('pages:main')
        else:
            context['client_form'] = client_form
            context['app_form'] = app_form
            try:
                test_time = str(request.POST['appointment_time'])
                object = datetime.strptime(test_time, '%H:%M')
            except:
                context['error'] = 'Введен неверный формат времени \n Пример: 12:00'
                return render(request, 'Appointment.html', context)
            if not re.match(r'^[\+]{1}[\d]+$', request.POST['telephone']):
                context['error'] = 'Неверный формат номера, пример: +380982794923'
                return render(request, 'Appointment.html', context)
            context['error'] = 'Данные введены неправильно'
            return render(request, 'Appointment.html', context)



def search(request):
    search_form = ClientSearchForm()
    context = {
        "title": "Поиск записей на прием",
        "search_form": search_form,
    }
    if request.method == 'GET':
        with connection.cursor() as cursor:
            query_app = f"SELECT c.First_name, c.Last_name, r.Date, time_of_appointment, d.First_name, d.Last_name, s.Name, a.appointment_id FROM appointment as a LEFT JOIN client as c ON a.client_id = c.client_id LEFT JOIN Reception_day as r on a.reception_day_id = r.reception_day_id LEFT JOIN Doctor as d on r.doctor_id = d.doctor_id LEFT JOIN appointment_status as s on a.status_id = s.status_id"
            cursor.execute(query_app)
            context['appointments'] = cursor.fetchall()
            print(context['appointments'])
        if request.session.get('call', '') == 1:
            context['confirmation_message'] = request.session.get('confirm_message', '')
            request.session['call'] = 0
        return render(request, 'Search.html', context)
    if request.method == 'POST':
        search_form = ClientSearchForm(request.POST)
        email = request.POST["email"]
        telephone = request.POST["telephone"]
        if search_form.is_valid():
            with connection.cursor() as cursor:
                query = f"SELECT Client_id FROM client WHERE Client_telephone = '{telephone}' AND Client_email = '{email}'"
                cursor.execute(query)
                result = cursor.fetchone()
                if str(result) == 'None':
                    context['error'] = 'Оформленных записей по поиску не найдено'
                    context['search_form'] = search_form
                    return render(request, 'Search.html', context)
                context['client_id'] = result[0]
                client_id = int(context['client_id'])
            with connection.cursor() as cursor:
                query_app = f"SELECT c.First_name, c.Last_name, r.Date, time_of_appointment, d.First_name, d.Last_name, s.Name, a.appointment_id FROM appointment as a LEFT JOIN client as c on a.client_id = c.client_id LEFT JOIN appointment_status as s on s.status_id = a.status_id LEFT JOIN reception_day as r on a.reception_day_id = r.reception_day_id LEFT JOIN doctor as d on d.doctor_id = r.doctor_id WHERE c.client_id = '{client_id}'"
                cursor.execute(query_app)
                context['appointments'] = cursor.fetchall()
                context['search_form'] = search_form
                print(context['appointments'])
            # return redirect('pages:shedule')
            return render(request, 'Search.html', context)
        else:
            context['error'] = 'Данные введены неправильно'
            context['search_form'] = search_form
            return render(request, 'Search.html', context)


def info(request):
    context = {
        "title": "Пациентам",
    }
    return render(request, 'Info.html', context)


def update(request, app_id):
    appointment = Appointment.objects.get(id=app_id)

    appointment_form = AppointmentFormChange(instance=Appointment.objects.get(id=app_id),
                                             initial={'date_last_change': f"{appointment.date_last_change}",
                                                      'appointment_time': f"{appointment.appointment_time.strftime('%H:%M')}"})
    context = {
        "title": "Обновление информации",
        'appointment_form': appointment_form
    }
    print(context)
    if request.method == 'GET':
        return render(request, 'Update.html', context)
    if request.method == 'POST':
        print('post')
        print(request.POST)
        form = AppointmentFormChange(request.POST, instance=Appointment.objects.get(id=app_id))
        appointment_form = AppointmentFormChange(request.POST)
        context['appointment_form'] = appointment_form
        if form.has_changed():
            app_client = request.POST['client']
            app_day = request.POST['reception_day']
            app_time = request.POST['appointment_time']
            app_status = request.POST['status']
            if form.is_valid():
                test_time = request.POST['appointment_time']
                if ':' in test_time[:2]:
                    test_time_hour = int(test_time[:1])
                    test_time_minute = int(test_time[2:])
                else:
                    test_time_minute = int(test_time[3:])
                    test_time_hour = int(test_time[:2])
                reception_day = ReceptionDay.objects.filter(id=request.POST['reception_day']).first()
                print(reception_day)
                appointments = Appointment.objects.filter(reception_day_id=request.POST['reception_day'])
                print(appointments)
                start_time_hour = reception_day.start_time.hour
                start_time_minute = reception_day.start_time.minute
                end_time_hour = reception_day.end_time.hour
                end_time_minute = reception_day.end_time.minute
                if test_time_hour < start_time_hour:
                    context['error'] = f"Введено неккоректное время приема \n Время начала приема: " \
                                       f"{reception_day.start_time.strftime('%H:%M')}"
                    return render(request, 'Update.html', context)
                elif test_time_hour == start_time_hour and test_time_minute < start_time_minute:
                    context['error'] = f"Введено неккоректное время приема \n Время начала приема: " \
                                       f"{reception_day.start_time.strftime('%H:%M')}"
                    return render(request, 'Update.html', context)
                elif (test_time_hour - end_time_hour) >= 0:
                    if test_time_minute >= end_time_minute:
                        context['error'] = f"Введено неккоректное время приема \n Время окончания приема: " \
                                           f"{reception_day.end_time.strftime('%H:%M')}"
                        return render(request, 'Update.html', context)
                    if abs(test_time_minute - end_time_minute) < 30:
                        context['error'] = f"Введено неккоректное время приема \n Время окончания приема: " \
                                           f"{reception_day.end_time.strftime('%H:%M')} \n Длительность приема: 30 минут"
                        return render(request, 'Update.html', context)
                elif (end_time_hour - test_time_hour) == 1:
                    if (60 - abs(test_time_minute - end_time_minute)) < 30:
                        context['error'] = f"Введено неккоректное время приема \n Время окончания приема: " \
                                           f"{reception_day.end_time.strftime('%H:%M')} \n Длительность приема: 30 минут"
                        return render(request, 'Update.html', context)

                for appointment in appointments:
                    print(appointment)
                    print('1')
                    if appointment.id != app_id:
                        print(appointment)
                        print(appointment)
                        minute = appointment.appointment_time.minute
                        print(minute)
                        hour = appointment.appointment_time.hour
                        print(hour)
                        if test_time_hour == hour:
                            if abs(minute - test_time_minute) < 30:
                                context['error'] = 'К сожалению, данное время уже занято, ближайшее свободное время ' \
                                                   'в выбранный день - '
                                return render(request, 'Update.html', context)
                        elif abs(test_time_hour - hour) <= 1:
                            if abs(60 - abs(minute - test_time_minute)) < 30:
                                context['error'] = 'К сожалению, данное время уже занято, ближайшее свободное время ' \
                                                   'в выбранный день - '
                                return render(request, 'Appointment.html', context)

                appointment = Appointment.objects.get(id=app_id)
                client = Client.objects.get(id=app_client)
                reception_day = ReceptionDay.objects.get(id=app_day)
                status = Status.objects.get(id=app_status)
                appointment.client = client
                appointment.reception_day = reception_day
                appointment.appointment_time = app_time
                appointment.date_last_change = date.today()
                appointment.status = status
                appointment.save()
                with connection.cursor() as cursor:
                    query = f"UPDATE appointment SET Time_of_appointment = '{app_time}', Reception_day_id = '{app_day}', Status_id = '{app_status}', Client_id = '{app_client}', Date_of_change = CURDATE() WHERE Appointment_id = '{app_id}'"
                    cursor.execute(query)
                with connection.cursor() as cursor:
                    query = f"SELECT Client_telephone, Client_email FROM client INNER JOIN appointment WHERE Appointment_id = '{app_id}'"
                    cursor.execute(query)
                    result = cursor.fetchone()
                    context['telephone'] = result[0]
                    context['email'] = result[1]
                    print(result)

                message = 'Информация выбранной записи на прием была успешна обновлена'
                request.session['confirm_message'] = message
                request.session['call'] = 1
                return redirect('pages:search')
            else:
                context['appointment_form'] = appointment_form
                try:
                    test_time = request.POST['appointment_time']
                    datetime.time(test_time)
                except:
                    context['error'] = 'Введен неверный формат времени. Пример: 12:00'
                    return render(request, 'Update.html', context)
                context['error'] = 'Данные введены неправильно'
                return render(request, 'Update.html', context)
        else:
            message = 'Никаких изменений информации в выбранную запись введено не было'
            request.session['confirm_message'] = message
            return redirect('pages:search')


def refuse(request, app_id):
    appointment_form = AppointmentFormChange(instance=Appointment.objects.get(id=app_id))
    context = {
        "title": "Отказ от записи на прием",
        'appointment_form': appointment_form
    }
    print(context)
    if request.method == 'GET':
        print('get')
        with connection.cursor() as cursor:
            query = f"SELECT Status_id FROM appointment_status WHERE Name='Отклонена'"
            cursor.execute(query)
            status_id = cursor.fetchone()[0]
        status = Status.objects.get(name='Отклонена')
        appointment = Appointment.objects.get(id=app_id)
        appointment.status = status
        appointment.save()
        with connection.cursor() as cursor:
            query = f"UPDATE appointment SET Status_id = '{status_id}' WHERE Appointment_id = '{app_id}'"
            cursor.execute(query)
        return redirect('pages:search')
    else:
        return redirect('pages:search')
