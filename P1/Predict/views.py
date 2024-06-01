# Create your views here.
from sklearn.tree import DecisionTreeClassifier
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from Student.models import Student, Class, CHOICESGENDER
from Attendance.models import Attendance
from Rate.models import Rate, CHOICESRATE
from Teacher.models import Teacher
from Class.models import Class
# Create your views here.
import joblib
import statistics
import os
CHOICEDISTANCE = [(0, 0), (5, 1), (15, 2)]
CHOICEDISTANCE_AS_CATEGORIES = [(0, "Dekat"), (1, "Sedang"), (2, "Jauh")]
RESULT = [(0, "Sangat Suka"), (1, "Lumayan Suka"), (2, "Tidak Suka")]
TEACHER = [("Misterboy", 0), ("Yanti", 1), ("Greece", 2)]
MODEL_DIRECTORY = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'models')


@login_required(login_url="User:login")
@permission_required('Predict.predict_one', login_url="permission_denied")
def predictionOne(request, id):
    try:
        # Cek ada data siswa ga
        nameStudent = Student.objects.get(id=id).name

        if not Attendance.objects.filter(id_student=id).exists():
            raise Attendance.DoesNotExist

        # Cek ada data absensi ga
        dataAttendance = list(Attendance.objects.filter(
            id_student=id).values_list('id', flat=True))

        # Cek ada data rate ga
        dataRate = list(Rate.objects.values_list(
            'id_attendance', flat=True))

        def boolRate(dataRate, dataAttendance):
            for n in dataRate:
                if n in dataAttendance:
                    return True
            raise Rate.DoesNotExist
        boolRate(dataRate, dataAttendance)

        data = list(Student.objects.filter(id=id).values())
        for n in data:
            for m in CHOICEDISTANCE:
                if n['distance'] >= m[0]:
                    distance = m[1]

        data = list(Student.objects.filter(
            id=id).values())
        for n in data:
            class_id = n['id_class_id']
            dataClass = list(Class.objects.filter(id=class_id).values())

            for m in dataClass:
                teacher_id = m['id_teacher_id']
                teacher_name = Teacher.objects.get(id=teacher_id).name

        for n in TEACHER:
            if n[0] == teacher_name:
                teacher = n[1]

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

        ml_model = joblib.load('ml_model/model3.joblib')
        result = ml_model.predict(
            [[distance, persentange_attendance, rate, teacher]])

        # return HttpResponse(result)
        for n in RESULT:
            if n[0] == result:
                result = n[1]
        return JsonResponse([distance, persentange_attendance, rate, teacher, result], safe=False)

    except Student.DoesNotExist as error:
        return HttpResponse(f"please make student data")
    except Attendance.DoesNotExist as error:
        return HttpResponse(f"please make attendance data")
    except Rate.DoesNotExist as error:
        return HttpResponse(f"please make rate data")


def prediction(id):
    try:
        # Cek ada data siswa ga
        dataStudent = Student.objects.get(id=id)

        ###################### buat data  distance ###############################
        data = list(Student.objects.filter(id=id).values())
        for n in data:
            for m in CHOICEDISTANCE:
                if n['distance'] >= m[0]:
                    distance = m[1]

        ######################## buat data teacher ###############################
        data = list(Student.objects.filter(
            id=id).values())
        for n in data:
            class_id = n['id_class_id']
            dataClass = list(Class.objects.filter(id=class_id).values())

            for m in dataClass:
                teacher_id = m['id_teacher_id']
                teacher_name = Teacher.objects.get(id=teacher_id).name

        for n in TEACHER:
            if n[0] == teacher_name:
                teacher = n[1]
        ###########################################################################

        # Cek ada data absensi ga
        if not Attendance.objects.filter(id_student=id).exists():
            raise Attendance.DoesNotExist
        ########################## buat data absensi################################

        dataAbsent = int(Attendance.objects.filter(
            id_student=id, status_attendance=0).values().count())
        dataPresent = int(Attendance.objects.filter(
            id_student=id, status_attendance=1).values().count())
        persentange_attendance = dataPresent / (dataAbsent+dataPresent)
        ###########################################################################

        # Cek ada data rate ga
        dataAttendance = list(Attendance.objects.filter(
            id_student=id).values_list('id', flat=True))

        dataRate = list(Rate.objects.values_list(
            'id_attendance', flat=True))

        def boolRate(dataRate, dataAttendance):
            for n in dataRate:
                if n in dataAttendance:
                    return True
            raise Rate.DoesNotExist
        boolRate(dataRate, dataAttendance)

        ########################## buat data rate #################################

        data = list(Attendance.objects.filter(
            id_student=id).values_list('id', flat=True))
        result = (list(Rate.objects.filter(
            id_attendance__in=data).values_list('rate', flat=True)))
        rate = round(statistics.mean(result))

        ml_model = joblib.load('ml_model/model3.joblib')
        result = ml_model.predict(
            [[distance, persentange_attendance, rate, teacher]])
        ###########################################################################

        for n in RESULT:
            if n[0] == result:
                resultML = n[1]
        return {'id': id, 'name': dataStudent.name, 'distance': distance, 'persentange_attendance': persentange_attendance*100, 'rate': rate, 'teacher': teacher_name, 'resultML': resultML}

    except Student.DoesNotExist:
        resultML = 'Please make student data'
        return {'id': id, 'name': dataStudent.name, 'resultML': resultML}
    except Attendance.DoesNotExist:
        resultML = "please make attendance data"
        return {'id': id, 'name': dataStudent.name, 'distance': distance, 'teacher': teacher_name, 'resultML': resultML}
    except Rate.DoesNotExist:
        resultML = "please make rate data"
        return {'id': id, 'name': dataStudent.name, 'distance': distance, 'persentange_attendance': persentange_attendance*100, 'teacher': teacher_name, 'resultML': resultML}


@login_required(login_url="User:login")
@permission_required('Predict.predict_all', login_url="permission_denied")
def choose(request):
    if request.method == "POST":
        data = request.POST.getlist('checkPresent')
        data = [int(item) for item in data]
        result = list()
        for n in data:
            result.append(prediction(n))
        # return JsonResponse(result, safe=False)
        return render(request, "predict/table_predict.html", {'form': result, 'choiceRate': CHOICESRATE, 'choiceDistance': CHOICEDISTANCE_AS_CATEGORIES})
    else:
        form = {
            'student': Student.objects.all(),
            'class': Class.objects.all(),
        }
        return render(request, "predict/list_predict.html", {'form': form})
