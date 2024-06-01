# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .forms import SaveForm
from .models import Rate, Attendance, CHOICESRATE
# Create your views here.


def read(request):
    message = ""
    message_tag = ""
    for msg in messages.get_messages(request):
        message = msg
        message_tag = msg.tags
    form = {
        'title': 'View Data',
        'data': Rate.objects.all(),
        'rate': CHOICESRATE,
        "message": str(message),
        "message_tag": message_tag
    }

    return render(request, "rate/read.html", {'form': form})

    # classs_list = list(Rate.objects.all().values())

    # # Mengembalikan data dalam format JSON
    # return JsonResponse(classs_list, safe=False)


def readDetail(request, id):
    try:
        form = {
            'title': 'View Data',
            'data': Rate.objects.get(id=id),
            'rate': CHOICESRATE,
            'attendance': Attendance.objects.all(),
        }

        return render(request, "rate/readDetail.html", {'form': form})
    except Exception as s:
        messages.error(request, s)
        return redirect("Rate:read")


# def create(request):
#     if request.method == "POST":
#         data = SaveForm(request.POST)
#         if data.is_valid():
#             data = data.save(commit=False)

#             data.author = request.user
#             data.save()
#             messages.success(request, "Data Berhasil dibuat")
#             return redirect('Rate:read')
#         else:
#             messages.error(request, data.errors)
#             return redirect('Rate:create')

#     else:
#         message = ""
#         message_tag = ""
#         for msg in messages.get_messages(request):
#             message = msg
#             message_tag = msg.tags
#         form = {
#             'title': 'Create Data',
#             'form': SaveForm(),
#             'attendance': Attendance.objects.all(),
#             "message": str(message),
#             "message_tag": message_tag
#         }

#         return render(request, "rate/create.html", {'form': form})

@login_required(login_url="User:login")
@permission_required('Rate.change_rate', login_url="permission_denied")
def update(request, id):
    try:
        initialData = Rate.objects.get(id=id)
        if request.method == "POST":
            data = SaveForm(request.POST, instance=initialData)
            if data.is_valid():
                data = data.save(commit=False)
                data.author = request.user
                data.save()
                messages.success(request, "Data Berhasil diubah")
                return redirect("Rate:read")
            else:
                messages.error(request, data.errors)
                return redirect("Rate:update")

        else:
            message = ""
            message_tag = ""
            for msg in messages.get_messages(request):
                message = msg
                message_tag = msg.tags

            form = {
                'title': 'Create Data',
                'form': SaveForm(instance=initialData),
                'attendance': Attendance.objects.all(),
                'rate': CHOICESRATE,
                "message": str(message),
                "message_tag": message_tag
            }
            return render(request, "rate/update.html", {'form': form})
    except Exception as s:
        messages.error(request, s)
        return redirect("Rate:read")


@login_required(login_url="User:login")
@permission_required('Rate.delete_rate', login_url="permission_denied")
def delete(request, id):
    try:
        data = Rate.objects.get(id=id)
        data.delete()
        messages.success(request, "Data Berhasil dihapus")
    except Exception as s:
        messages.error(request, s)
    return redirect("Rate:read")


@login_required(login_url="User:login")
@permission_required('Rate.add_rate', login_url="permission_denied")
def createDataRate_Attendance(request):
    data = SaveForm(request.POST)
    if data.is_valid():
        data = data.save(commit=False)

        data.author = request.user
        data.save()
        messages.success(request, "Data Berhasil dibuat")
        return redirect('Attendance:read')
    else:
        messages.error(request, data.errors)
        return redirect('Rate:read')
