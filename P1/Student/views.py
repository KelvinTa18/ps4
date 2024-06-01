# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .forms import SaveForm
from .models import Student, Class, CHOICESGENDER
from Attendance.models import Attendance
from Rate.models import Rate
# Create your views here.
import statistics


def read(request):
    message = ""
    message_tag = ""
    for msg in messages.get_messages(request):
        message = msg
        message_tag = msg.tags
    form = {
        'title': 'View Data',
        'data': Student.objects.all(),
        'gender': CHOICESGENDER,
        "message": str(message),
        "message_tag": message_tag
    }

    return render(request, "student/read.html", {'form': form})

    # classs_list = list(Student.objects.all().values())

    # # Mengembalikan data dalam format JSON
    # return JsonResponse(classs_list, safe=False)


def readDetail(request, id):
    try:
        form = {
            'title': 'View Data',
            'data': Student.objects.get(id=id),
            'gender': CHOICESGENDER,
            'class': Class.objects.all(),
        }

        return render(request, "student/readDetail.html", {'form': form})
    except Exception as s:
        messages.error(request, s)
        return redirect("Student:read")


@login_required(login_url="User:login")
@permission_required('Student.add_student', login_url="permission_denied")
def create(request):
    if request.method == "POST":
        data = SaveForm(request.POST)
        if data.is_valid():
            data = data.save(commit=False)
            data.author = request.user
            data.save()
            messages.success(request, "Data Berhasil dibuat")
            return redirect('Student:read')
        else:
            messages.error(request, data.errors)
            return redirect('Student:create')

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
            'gender': CHOICESGENDER,
            "message": str(message),
            "message_tag": message_tag
        }

        return render(request, "student/create.html", {'form': form})


@login_required(login_url="User:login")
@permission_required('Student.change_student', login_url="permission_denied")
def update(request, id):
    try:
        initialData = Student.objects.get(id=id)
        if request.method == "POST":
            data = SaveForm(request.POST, instance=initialData)
            if data.is_valid():
                data = data.save(commit=False)
                data.author = request.user
                data.save()
                messages.success(request, "Data Berhasil diubah")
                return redirect("Student:read")
            else:
                messages.error(request, data.errors)
                return redirect("Student:update")

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
                'gender': CHOICESGENDER,
                "message": str(message),
                "message_tag": message_tag
            }
            return render(request, "student/update.html", {'form': form})
    except Exception as s:
        messages.error(request, s)
        return redirect("Student:read")


@login_required(login_url="User:login")
@permission_required('Student.delete_student', login_url="permission_denied")
def delete(request, id):
    try:
        data = Student.objects.get(id=id)
        data.delete()
        messages.success(request, "Data Berhasil dihapus")
    except Exception as s:
        messages.error(request, s)
    return redirect("Student:read")


def predict(request, id):
    ################## jarak ###################
    # data = list(Student.objects.filter(id=id).values())
    # for n in data:
    #     distance = n['distance']
    # return HttpResponse(distance)
    ############################################

    ################ teacher ###################
    # data = list(Student.objects.filter(id=id).values())
    # for n in data:
    #     teacher = n['id_class_id']
    # return HttpResponse(teacher)
    ############################################

    ############### attendance #################
    # dataAbsent = int(Attendance.objects.filter(
    #     id_student=id, status_attendance=0).values().count())
    # dataPresent = int(Attendance.objects.filter(
    #     id_student=id, status_attendance=1).values().count())
    # return HttpResponse(dataPresent / (dataAbsent+dataPresent))
    ############################################

    ############# kepuasan (rate) ##############
    # data = list(Attendance.objects.filter(
    #     id_student=id).values_list('id', flat=True))
    # result = (list(Rate.objects.filter(
    #     id_attendance__in=data).values_list('rate', flat=True)))
    # rate = round(statistics.mean(result))
    # return HttpResponse(rate)
    ############################################

    data = list(Student.objects.filter(id=id).values())
    for n in data:
        distance = n['distance']

    data = list(Student.objects.filter(id=id).values())
    for n in data:
        teacher = n['id_class_id']

    dataAbsent = int(Attendance.objects.filter(
        id_student=id, status_attendance=0).values().count())
    dataPresent = int(Attendance.objects.filter(
        id_student=id, status_attendance=1).values().count())
    persentange_attendance = dataPresent / (dataAbsent+dataPresent)

    data = list(Attendance.objects.filter(
        id_student=id).values_list('id', flat=True))
    result = (list(Rate.objects.filter(
        id_attendance__in=data).values_list('rate', flat=True)))
    rate = round(statistics.mean(result))

    result = [distance, persentange_attendance, rate, teacher]
    return JsonResponse(result, safe=False)
