# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .forms import SaveForm
from .models import Teacher, CHOICESGENDER
# Create your views here.


@login_required(login_url="User:login")
def read(request):
    message = ""
    message_tag = ""
    for msg in messages.get_messages(request):
        message = msg
        message_tag = msg.tags
    form = {
        'title': 'View Data',
        'data': Teacher.objects.all(),
        'gender': CHOICESGENDER,
        "message": str(message),
        "message_tag": message_tag
    }

    return render(request, "teacher/read.html", {'form': form})

    # teachers_list = list(Teacher.objects.all().values())

    # # Mengembalikan data dalam format JSON
    # return JsonResponse(teachers_list, safe=False)


def readDetail(request, id):
    try:
        form = {
            'title': 'View Data',
            'data': Teacher.objects.get(id=id),
            'gender': CHOICESGENDER
        }

        return render(request, "teacher/readDetail.html", {'form': form})

    except Exception as s:
        messages.error(request, s)
        return redirect("Teacher:read")


@login_required(login_url="User:login")
@permission_required('Teacher.add_teacher', login_url="permission_denied")
def create(request):
    if request.method == "POST":
        data = SaveForm(request.POST)
        if data.is_valid():
            data = data.save(commit=False)
            data.author = request.user
            data.save()
            messages.success(request, "Data Berhasil dibuat")
            return redirect('Teacher:read')
        else:
            messages.error(request, data.errors)
            return redirect('Teacher:create')

    else:
        message = ""
        message_tag = ""
        for msg in messages.get_messages(request):
            message = msg
            message_tag = msg.tags
        form = {
            'title': 'Create Data',
            'form': SaveForm(),
            'gender': CHOICESGENDER,
            "message": str(message),
            "message_tag": message_tag
        }

        return render(request, "teacher/create.html", {'form': form})
    # if request.method == "POST":
    #     data = SaveForm(request.POST)
    #     if data.is_valid():
    #         data = data.save(commit=False)
    #         data.author = request.user
    #         data.save()
    #         messages.success(request, "Data Berhasil dibuat")
    #         return redirect('Teacher:read')
    #     else:
    #         messages.error(request, data.errors)
    #         return redirect('Teacher:create')

    # else:
    #     message = ""
    #     message_tag = ""
    #     for msg in messages.get_messages(request):
    #         message = msg
    #         message_tag = msg.tags
    #     form = {
    #         'title': 'Create Data',
    #         'form': SaveForm(),
    #         'gender': CHOICESGENDER,
    #         "message": str(message),
    #         "message_tag": message_tag
    #     }

    #     return render(request, "teacher/create.html", {'form': form})


@login_required(login_url="User:login")
@permission_required('Teacher.change_teacher', login_url="permission_denied")
def update(request, id):
    try:
        initialData = Teacher.objects.get(id=id)
        if request.method == "POST":
            data = SaveForm(request.POST, instance=initialData)
            if data.is_valid():
                data = data.save(commit=False)
                data.author = request.user
                data.save()
                messages.success(request, "Data Berhasil diubah")
                return redirect("Teacher:read")
            else:
                messages.error(request, data.errors)
                return redirect("Teacher:update")

        else:
            message = ""
            message_tag = ""
            for msg in messages.get_messages(request):
                message = msg
                message_tag = msg.tags

            form = {
                'title': 'Create Data',
                'form': SaveForm(instance=initialData),
                'gender': CHOICESGENDER,
                "message": str(message),
                "message_tag": message_tag
            }
            return render(request, "teacher/update.html", {'form': form})
    except Exception as s:
        messages.error(request, s)
        return redirect("Teacher:read")


@login_required(login_url="User:login")
@permission_required('Teacher.delete_teacher2', login_url="permission_denied")
def delete(request, id):
    try:
        data = Teacher.objects.get(id=id)
        data.delete()
        messages.success(request, "Data Berhasil dihapus")
    except Exception as s:
        messages.error(request, s)
    finally:
        return redirect("Teacher:read")


def permission(request):
    user = request.user
    all_permissions = user.get_all_permissions()
    # Mengkonversi set ke list jika diperlukan untuk template
    all_permissions_list = list(all_permissions)

    return JsonResponse(all_permissions_list, safe=False)
