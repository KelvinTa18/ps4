# Create your views here.
from django.db.models import ProtectedError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .forms import SaveForm
from .models import Class, Teacher

# Create your views here.
# Create your views here.


def read(request):
    message = ""
    message_tag = ""
    for msg in messages.get_messages(request):
        message = msg
        message_tag = msg.tags
    form = {
        'title': 'View Data',
        'data': Class.objects.all(),
        "message": str(message),
        "message_tag": message_tag
    }

    return render(request, "class/read.html", {'form': form})

    # teachers_list = list(Class.objects.all().values())

    # # Mengembalikan data dalam format JSON
    # return JsonResponse(teachers_list, safe=False)


def readDetail(request, id):
    try:
        form = {
            'title': 'View Data',
            'data': Class.objects.get(id=id),
            'teacher': Teacher.objects.all()
        }

        return render(request, "class/readDetail.html", {'form': form})
    except Exception as s:
        messages.error(request, s)
        return redirect("Class:read")


@login_required(login_url="User:login")
@permission_required('Class.add_class', login_url="permission_denied")
def create(request):
    if request.method == "POST":
        data = SaveForm(request.POST)
        if data.is_valid():
            data = data.save(commit=False)
            data.author = request.user
            data.save()
            messages.success(request, "Data Berhasil dibuat")
            return redirect('Class:read')
        else:
            messages.error(request, data.errors)
            return redirect('Class:create')

    else:
        message = ""
        message_tag = ""
        for msg in messages.get_messages(request):
            message = msg
            message_tag = msg.tags
        form = {
            'title': 'Create Data',
            'form': SaveForm(),
            'teacher': Teacher.objects.all(),
            "message": str(message),
            "message_tag": message_tag
        }

        return render(request, "class/create.html", {'form': form})


@login_required(login_url="User:login")
@permission_required('Class.change_class', login_url="permission_denied")
def update(request, id):
    try:
        initialData = Class.objects.get(id=id)
        if request.method == "POST":
            data = SaveForm(request.POST, instance=initialData)
            if data.is_valid():
                data = data.save(commit=False)
                data.author = request.user
                data.save()
                messages.success(request, "Data Berhasil diubah")
                return redirect("Class:read")
            else:
                messages.error(request, data.errors)
                return redirect("Class:update")

        else:
            message = ""
            message_tag = ""
            for msg in messages.get_messages(request):
                message = msg
                message_tag = msg.tags

            form = {
                'title': 'Create Data',
                'form': SaveForm(instance=initialData),
                'teacher': Teacher.objects.all(),
                "message": str(message),
                "message_tag": message_tag
            }
            return render(request, "class/update.html", {'form': form})
    except Exception as s:
        messages.error(request, s)
        return redirect("Class:read")


@login_required(login_url="User:login")
@permission_required('Class.delete_class', login_url="permission_denied")
def delete(request, id):
    try:
        data = Class.objects.get(id=id)
        data.delete()
        messages.success(request, "Data Berhasil dihapus")
    except Exception as s:
        messages.error(request, s)
    return redirect("Class:read")
