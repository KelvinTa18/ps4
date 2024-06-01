# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .forms import SaveForm
from .models import Schedule, Class
from Student.models import Student
from Attendance.models import Attendance
from Attendance.views import createDataAttendance_Schedule, updateDataAttendance_Schedule
from django.forms.models import model_to_dict
import json
from django.core import serializers
# Create your views here.


def read(request):
    message = ""
    message_tag = ""
    for msg in messages.get_messages(request):
        message = msg
        message_tag = msg.tags
    form = {
        'title': 'View Data',
        'data': Schedule.objects.all(),
        "message": str(message),
        "message_tag": message_tag
    }

    return render(request, "schedule/read.html", {'form': form})

    # classs_list = list(Schedule.objects.all().values())

    # # Mengembalikan data dalam format JSON
    # return JsonResponse(classs_list, safe=False)


def readDetail(request, id):
    try:
        form = {
            'title': 'View Data',
            'data': Schedule.objects.get(id=id),
            'class': Class.objects.all(),
        }

        return render(request, "schedule/readDetail.html", {'form': form})
    except Exception as s:
        messages.error(request, s)
        return redirect("Schedule:read")


@login_required(login_url="User:login")
@permission_required('Schedule.add_schedule', login_url="permission_denied")
def create(request):
    if request.method == "POST":
        data = SaveForm(request.POST)
        if data.is_valid():
            data = data.save(commit=False)

            data.author = request.user
            data.save()
            student_with_class = list(Student.objects.filter(
                id_class=data.class_id).values())

            createDataAttendance_Schedule(
                request.user, data, *student_with_class)
            messages.success(request, "Data Berhasil dibuat")
            return redirect('Schedule:read')
        else:
            messages.error(request, data.errors)
            return redirect('Schedule:create')

    else:
        message = ""
        message_tag = ""
        for msg in messages.get_messages(request):
            message = msg
            message_tag = msg.tags
        form = {
            'title': 'Create Data',
            'form': SaveForm(),
            'class': Class.objects.all(),
            "message": str(message),
            "message_tag": message_tag
        }

        return render(request, "schedule/create.html", {'form': form})


@login_required(login_url="User:login")
@permission_required('Schedule.change_schedule', login_url="permission_denied")
def update(request, id):
    try:
        initialData = Schedule.objects.get(id=id)
        if request.method == "POST":
            data = SaveForm(request.POST, instance=initialData)
            if data.is_valid():
                data = data.save(commit=False)
                data.author = request.user
                data.save()
                messages.success(request, "Data Berhasil diubah")
                return redirect("Schedule:read")
            else:
                messages.error(request, data.errors)
                return redirect("Schedule:update")

        else:
            message = ""
            message_tag = ""
            for msg in messages.get_messages(request):
                message = msg
                message_tag = msg.tags

            form = {
                'title': 'Create Data',
                'form': SaveForm(instance=initialData),
                'class': Class.objects.all(),
                "message": str(message),
                "message_tag": message_tag
            }
            return render(request, "schedule/update.html", {'form': form})
    except Exception as s:
        messages.error(request, s)
        return redirect("Schedule:read")


@login_required(login_url="User:login")
@permission_required('Schedule.delete_schedule', login_url="permission_denied")
def delete(request, id):
    try:
        data = Schedule.objects.get(id=id)
        data.delete()
        messages.success(request, "Data Berhasil dihapus")
    except Exception as s:
        messages.error(request, s)
    return redirect("Schedule:read")


@login_required(login_url="User:login")
@permission_required('Attendance.list_attendance', login_url="permission_denied")
def list_attendance(request, id):
    initialData = Schedule.objects.get(id=id)
    if request.method == "POST":
        selected_names = None
        data = request.POST.getlist('checkPresent')
        # data = json.dumps(dict(request.POST.getlist('checkPresent')))
        # return JsonResponse(data, safe=False)
        updateDataAttendance_Schedule(request.user, id, *data)
        messages.success(request, "Data Attendance diubah")
        return redirect("Schedule:read")

    else:
        form = {
            'form': SaveForm(instance=initialData),
            'class': Class.objects.all(),
            # 'student_with_class': Student.objects.filter(
            #     id_class=Schedule.objects.get(id=id).class_id.id).values()
            'student_with_class': Attendance.objects.filter(id_schedule=id)
        }
    # data = list(data)
    # if not data:
    #     return HttpResponse("NOne")
    # return JsonResponse(data, safe=False)

    return render(request, "schedule/list_attendance.html", {'form': form})
