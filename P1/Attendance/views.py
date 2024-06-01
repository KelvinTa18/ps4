# Create your views here.
from django import template
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .forms import SaveForm
from .models import Attendance, Schedule, Student, CHOICESATTENDACE
from Rate.models import Rate, CHOICESRATE
# Create your views here.

register = template.Library()


def read(request):
    message = ""
    message_tag = ""
    for msg in messages.get_messages(request):
        message = msg
        message_tag = msg.tags
    # data = Attendance.objects.all()
    # for n in data:
    #     n['newData'] = 1
    # data = list(data.values())
    listRate = [list(Rate.objects.all().values_list(
        'id_attendance', flat=True))][0]
    form = {
        'title': 'View Data',
        'data': Attendance.objects.all(),
        'status': CHOICESATTENDACE,
        'rate': Rate.objects.all(),
        'choiceRate': CHOICESRATE,
        'list': listRate,
        "message": str(message),
        "message_tag": message_tag
    }

    return render(request, "attendance/read.html", {'form': form})

    # classs_list = list(Attendance.objects.all().values())

    # # Mengembalikan data dalam format JSON
    # return JsonResponse(classs_list, safe=False)


def readDetail(request, id):
    try:
        form = {
            'title': 'View Data',
            'data': Attendance.objects.get(id=id),
            'schedule': Schedule.objects.all(),
            'student': Student.objects.all(),
            'status': CHOICESATTENDACE,
        }

        return render(request, "attendance/readDetail.html", {'form': form})
    except Exception as s:
        messages.error(request, s)
        return redirect("Attendance:read")


@login_required(login_url="User:login")
@permission_required('Attendance.add_attendance', login_url="permission_denied")
def create(request):
    if request.method == "POST":
        data = SaveForm(request.POST)
        if data.is_valid():
            data = data.save(commit=False)
            data.author = request.user
            data.save()
            messages.success(request, "Data Berhasil dibuat")
            return redirect('Attendance:read')
        else:
            messages.error(request, data.errors)
            return redirect('Attendance:create')

    else:
        message = ""
        message_tag = ""
        for msg in messages.get_messages(request):
            message = msg
            message_tag = msg.tags
        form = {
            'title': 'Create Data',
            'form': SaveForm(),
            'schedule': Schedule.objects.all(),
            'student': Student.objects.all(),
            'status': CHOICESATTENDACE,
            "message": str(message),
            "message_tag": message_tag
        }

        return render(request, "attendance/create.html", {'form': form})


@login_required(login_url="User:login")
@permission_required('Attendance.change_attendance', login_url="permission_denied")
def update(request, id):
    try:
        initialData = Attendance.objects.get(id=id)
        if request.method == "POST":
            data = SaveForm(request.POST, instance=initialData)
            if data.is_valid():
                data = data.save(commit=False)
                data.author = request.user
                data.save()
                messages.success(request, "Data Berhasil diubah")
                return redirect("Attendance:read")
            else:
                messages.error(request, data.errors)
                return redirect("Attendance:update")

        else:
            message = ""
            message_tag = ""
            for msg in messages.get_messages(request):
                message = msg
                message_tag = msg.tags

            form = {
                'title': 'Create Data',
                'form': SaveForm(instance=initialData),
                'schedule': Schedule.objects.all(),
                'student': Student.objects.all(),
                'status': CHOICESATTENDACE,
                "message": str(message),
                "message_tag": message_tag
            }
            return render(request, "attendance/update.html", {'form': form})
    except Exception as s:
        messages.error(request, s)
        return redirect("Attendance:read")


def delete(request, id):
    try:
        data = Attendance.objects.get(id=id)
        data.delete()
        messages.success(request, "Data Berhasil dihapus")
    except Exception as s:
        messages.error(request, s)
    return redirect("Attendance:read")


def createDataAttendance_Schedule(user, dataSchedule, *data):
    # data = SaveForm(request.POST)
    # if data.is_valid():
    #     data = data.save(commit=False)
    #     data.author = request.user
    #     data.save()
    #     messages.success(request, "Data Berhasil dibuat")
    #     return redirect('Attendance:read')
    for n in data:
        data = Attendance()
        data.id_schedule = dataSchedule
        dataStudent = Student.objects.get(id=n['id'])
        data.id_student = dataStudent
        data.status_attendance = 0
        data.author = user
        data.save()


def updateDataAttendance_Schedule(user, id_schedule, *data):
    data = [int(item) for item in data]
    for n in data:
        checkData = Attendance.objects.get(id=n)
        if (checkData.status_attendance == 0):
            checkData.status_attendance = 1
            checkData.author = user
            checkData.save()
            # change status_attendance to 1

    checkData = Attendance.objects.filter(
        status_attendance=1, id_schedule=id_schedule)

    for n in checkData:
        if (n.status_attendance == 1) and (n.id not in data):
            # change status_attendance to 0
            n.status_attendance = 0
            n.save()
