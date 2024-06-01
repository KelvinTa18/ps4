from django.shortcuts import render, redirect
from collections import defaultdict
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from Attendance.models import Attendance
from django.core.serializers import serialize
from datetime import datetime, timedelta
from django.contrib.auth import login, logout, authenticate

from django.db.models.functions import TruncMonth


def dashboard(request):
    form = {
        "title": "My Dashboard",
        "content": "MY CONTENT"
    }
    return render(request, "dashboard.html", {'form': form})


def permission_denied(request):
    if request.method == "POST":
        if 'next' in request.POST:
            path = str(request.POST.get('next')).split('/')[1]
            return redirect(f"/{path}")
            # return HttpResponse(f"/{path}")
    else:
        form = {
            "title": "Permission Denied",
            "content": "You dont have permission, Please contact the admin to continue with this action",
        }
        return render(request, "permission_denied.html", {'form': form})
