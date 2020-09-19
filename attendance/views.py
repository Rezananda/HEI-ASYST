from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from attendance.models import UserAttendance
from account.models import UserProfile
from datetime import datetime
from django.utils import timezone, dateformat
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_protect
import json

# Create your views here.
@csrf_protect
@login_required
def index(request):
    getUserId = UserProfile.objects.get(full_name = request.session['full_name'])
    # print(dateformat.format(timezone.now(), 'Y-m-d H:i:s'))
    try:
        getLatesAttend = UserAttendance.objects.filter(authors_id = getUserId.user_id).latest('id')

        def checkAttend():
            getdate = datetime.now().strftime('%Y-%m-%d')
            # print(getdate)
            # print(getLatesAttend.created_at)
            if getdate in str(getLatesAttend.created_at):
                return 'SUDAH'
            else:
                return 'BELUM'

        context = {
            'attend' : True,
            'full_name' : request.session['full_name'],
            'date' : getLatesAttend.created_at,
            'attend' : getLatesAttend.attendance,
            'condition' : getLatesAttend.condition,
            'work_status' : getLatesAttend.work_status,
            'status_attend' : checkAttend()
        }

        return render(request, 'attendance/index.html', context)
        
    except UserAttendance.DoesNotExist:
        context = {
            'attend' : False,
            'full_name' : request.session['full_name'],
        }

        return render(request, 'attendance/index.html', context)
    
    context = {
        'full_name' : request.session['full_name'],
        'date' : getLatesAttend.created_at
    }
    
    return render(request, 'attendance/index.html', context)

@login_required()
def all_attendance(request):
    getdate = datetime.now().strftime('%Y-%m-%d')
    getAllData = UserAttendance.objects.filter(created_at__date = getdate)

    getFullName = []
    for i in getAllData:
        getUserId = UserProfile.objects.get(user = i.authors)
        getFullName.append(getUserId.full_name)

    context = {
        'data' : getFullName,
        'full_name' : request.session['full_name'],
    }
    return render(request, 'attendance/all_attendance.html', context)

@login_required
def my_attendance(request):
    getUserId = UserProfile.objects.get(full_name = request.session['full_name'])

    getSehatCondition = UserAttendance.objects.filter(authors_id = getUserId.user_id, condition = 'Sehat').count()
    getSakitCondition = UserAttendance.objects.filter(authors_id = getUserId.user_id, condition = 'Sakit').count()
    
    kondisi = []
    kondisi.append(getSehatCondition)
    kondisi.append(getSakitCondition)

    getHadirCondition = UserAttendance.objects.filter(authors_id = getUserId.user_id, attendance = 'Hadir').count()
    getTidakHadirCondition = UserAttendance.objects.filter(authors_id = getUserId.user_id, attendance = 'Tidak Hadir').count()

    kehadiran = []
    kehadiran.append(getHadirCondition)
    kehadiran.append(getTidakHadirCondition)

    print(kehadiran)

    context = {
        'full_name' : request.session['full_name'],
        'attend' : kehadiran,
        'condition' : kondisi
    }

    return render(request, 'attendance/my_attendance.html', context)

@login_required
def my_attendance_list(request):
    getUserId = UserProfile.objects.get(full_name = request.session['full_name'])

    getListAttendance = UserAttendance.objects.filter(authors_id = getUserId.user_id).all().order_by('created_at')

    context = {
        'full_name' : request.session['full_name'],
        'attendance' : getListAttendance,
        'url' : 'DAFTAR DATA',
        'back_url' : '/'
    }

    return render(request, 'attendance/my_attendance_list.html', context)

@login_required
def my_attendance_detail(request, id):

    getAttendanceDetail = UserAttendance.objects.get(id = id)
    
    getDate = timezone.localtime(getAttendanceDetail.created_at)

    data = {
        'selfass' : getAttendanceDetail.selfassstatus,
        'attendance' : getAttendanceDetail.attendance,
        'reasonNotPresent' : getAttendanceDetail.reasonNotPresent,
        'otherNotPresent' : getAttendanceDetail.otherNotPresent,
        'condition' : getAttendanceDetail.condition,
        'sickChoices' : getAttendanceDetail.sickChoices,
        'otherSicks' : getAttendanceDetail.otherSicks,
        'work_status' : getAttendanceDetail.work_status,
        'wfo_description' : getAttendanceDetail.wfo_description,
        'date_created' : getDate.strftime("%d-%m-%Y"),
        'time_created' : getDate.strftime("%H:%M"),
        
        'id' : getAttendanceDetail.id
    }

    return JsonResponse({'attendance':data}, status=200)


@login_required
def my_attendance_edit(request, id):
    
    if request.method == 'POST':
        
        attendance = UserAttendance.objects.get(id = id)

        attendance.attend = request.POST.get('attend')
        attendance.reasonAttends = request.POST.get('reasonAttends')
        attendance.otherAttend = request.POST.get('otherAttend')
        attendance.condition = request.POST.get('condition')
        attendance.sickChoices = request.POST.get('sickChoices')
        attendance.otherSicks = request.POST.get('otherSicks')
        attendance.work_status = request.POST.get('work_status')
        attendance.work_description = request.POST.get('work_description')
        attendance.authors = request.user
        attendance.save()

        messages.success(request, 'Berhasil ubah data!')

        return redirect('my_attendance_edit', id=id)

    elif request.method == 'GET':
        getAttendanceDetail = UserAttendance.objects.get(id = id)

        context = {
            'full_name' : request.session['full_name'],
            'data' : getAttendanceDetail,
            'url' : 'UBAH DATA',
            'back_url' : '/my-attend-list'
        }

        return render(request, 'attendance/my_attendance_edit.html', context)

@login_required
def more(request):
    context = {
        'full_name' : request.session['full_name']
    }
    return render(request, 'attendance/more.html', context)

@login_required
def add_attend(request):

    if request.method == 'POST':

        attendance = UserAttendance()

        attendance.selfassstatus = request.POST.get('selfass')
        attendance.attendance = request.POST.get('attend')
        attendance.reasonNotPresent = request.POST.get('reasonAttends')
        attendance.otherNotPresent = request.POST.get('otherAttend')
        attendance.condition = request.POST.get('condition')
        attendance.sickChoices = request.POST.get('sickChoices')
        attendance.otherSicks = request.POST.get('otherSicks')
        attendance.work_status = request.POST.get('work_status')
        attendance.wfo_description = request.POST.get('work_description')
        attendance.authors = request.user

        attendance.save()

        messages.success(request, 'Berhasil tambah data!')
        return redirect('all_attendance')
    else:

        context = {
            'url' : 'TAMBAH DATA',
            'back_url' : '/'
        }

        return render(request, 'attendance/add_attend.html', context)

@login_required
def add_edit_attend(request):
    if request.method == 'POST':
        attendance = UserAttendance()

        attendance.attend = request.POST.get('attend')
        attendance.reasonAttends = request.POST.get('reasonAttends')
        attendance.otherAttend = request.POST.get('otherAttend')
        attendance.condition = request.POST.get('condition')
        attendance.sickChoices = request.POST.get('sickChoices')
        attendance.otherSicks = request.POST.get('otherSicks')
        attendance.work_status = request.POST.get('work_status')
        attendance.work_description = request.POST.get('work_description')
        attendance.authors = request.user
        attendance.save()

        messages.success(request, 'Berhasil tambah data!')
        return redirect('all_attendance')

    else:
        getUserId = UserProfile.objects.get(full_name = request.session['full_name'])
        getLatesAttend = UserAttendance.objects.filter(authors_id = getUserId.user_id).latest('id')

        context = {
            'data' : getLatesAttend,
            'full_name' : request.session['full_name'],
            'url' : 'TAMBAH DATA',
            'back_url' : '/'
        }

        return render(request, 'attendance/add_edit_attend.html', context)

@login_required
def add_same_attend(request):

    getUserId = UserProfile.objects.get(full_name = request.session['full_name'])
    getLatesAttend = UserAttendance.objects.filter(authors_id = getUserId.user_id).latest('id')

    attendance = UserAttendance()

    attendance.attend = getLatesAttend.attend
    attendance.reasonAttends = getLatesAttend.reasonAttends
    attendance.otherAttend = getLatesAttend.otherAttend
    attendance.condition = getLatesAttend.condition
    attendance.sickChoices = getLatesAttend.sickChoices
    attendance.otherSicks = getLatesAttend.otherSicks
    attendance.work_status = getLatesAttend.work_status
    attendance.work_description = getLatesAttend.work_description
    attendance.authors = request.user

    attendance.save()

    messages.success(request, 'Berhasil tambah data!')
    return redirect('all_attendance')

@login_required()
def manager_page(request):

    getDate = request.GET.get('date', '')
    getdateNow = datetime.now().strftime('%Y-%m-%d')

    if getDate == 'now':
        
        getSehatCondition = UserAttendance.objects.filter(condition = 'Sehat', created_at__date = getdateNow).count()
        getSakitCondition = UserAttendance.objects.filter(condition = 'Sakit', created_at__date = getdateNow).count()

        getSehatCondition = UserAttendance.objects.filter(condition = 'Sehat', created_at__date = getdateNow).count()
        getSakitCondition = UserAttendance.objects.filter(condition = 'Sakit', created_at__date = getdateNow).count()
    
        kondisi = []

        kondisi.append(getSehatCondition)
        kondisi.append(getSakitCondition)

        getHadirCondition = UserAttendance.objects.filter(attendance = 'Hadir', created_at__date = getdateNow).count()
        getTidakHadirCondition = UserAttendance.objects.filter(attendance = 'Tidak Hadir', created_at__date = getdateNow).count()

        kehadiran = []
        kehadiran.append(getHadirCondition)
        kehadiran.append(getTidakHadirCondition)
        
        getAuthor = UserAttendance.objects.filter(condition = 'Sakit', created_at__date = getdateNow)
    
        getFullNameSakit = []
        for i in getAuthor:
            getFullNameByAuthor = UserProfile.objects.get(user = i.authors)
            getFullNameSakit.append(getFullNameByAuthor.full_name)

        getAllData = UserAttendance.objects.filter(created_at__date = getdateNow)

        context = {
            'attend' : kehadiran,
            'condition' : kondisi,
            'sick_name' : getFullNameSakit,
            'attendance' : getAllData,
            'datenow' : getdateNow
        }
        return render(request, 'attendance/manager_page.html', context)

    elif getDate == 'all':

        getSehatCondition = UserAttendance.objects.filter(condition = 'Sehat').count()
        getSakitCondition = UserAttendance.objects.filter(condition = 'Sakit').count()

        getSehatCondition = UserAttendance.objects.filter(condition = 'Sehat').count()
        getSakitCondition = UserAttendance.objects.filter(condition = 'Sakit').count()
    
        kondisi = []

        kondisi.append(getSehatCondition)
        kondisi.append(getSakitCondition)

        getHadirCondition = UserAttendance.objects.filter(attendance = 'Hadir').count()
        getTidakHadirCondition = UserAttendance.objects.filter(attendance = 'Tidak Hadir').count()

        kehadiran = []
        kehadiran.append(getHadirCondition)
        kehadiran.append(getTidakHadirCondition)
        
        getAuthor = UserAttendance.objects.filter(condition = 'Sakit', created_at__date = getdateNow)
    
        getFullNameSakit = []
        for i in getAuthor:
            getFullNameByAuthor = UserProfile.objects.get(user = i.authors)
            getFullNameSakit.append(getFullNameByAuthor.full_name)

        getAllData = UserAttendance.objects.all()

        context = {
            'attend' : kehadiran,
            'condition' : kondisi,
            'sick_name' : getFullNameSakit,
            'attendance' : getAllData,
            'datenow' : getdateNow
        }
        return render(request, 'attendance/manager_page.html', context)

    else:

        getSehatCondition = UserAttendance.objects.filter(condition = 'Sehat', created_at__date = getDate).count()
        getSakitCondition = UserAttendance.objects.filter(condition = 'Sakit', created_at__date = getDate).count()

        getSehatCondition = UserAttendance.objects.filter(condition = 'Sehat', created_at__date = getDate).count()
        getSakitCondition = UserAttendance.objects.filter(condition = 'Sakit', created_at__date = getDate).count()
    
        kondisi = []

        kondisi.append(getSehatCondition)
        kondisi.append(getSakitCondition)

        getHadirCondition = UserAttendance.objects.filter(attendance = 'Hadir', created_at__date = getDate).count()
        getTidakHadirCondition = UserAttendance.objects.filter(attendance = 'Tidak Hadir', created_at__date = getDate).count()

        kehadiran = []
        kehadiran.append(getHadirCondition)
        kehadiran.append(getTidakHadirCondition)
        
        getAuthor = UserAttendance.objects.filter(condition = 'Sakit', created_at__date = getdateNow)
    
        getFullNameSakit = []
        for i in getAuthor:
            getFullNameByAuthor = UserProfile.objects.get(user = i.authors)
            getFullNameSakit.append(getFullNameByAuthor.full_name)

        getAllData = UserAttendance.objects.filter(created_at__date = getDate)

        print(getAllData)

        context = {
            'attend' : kehadiran,
            'condition' : kondisi,
            'sick_name' : getFullNameSakit,
            'attendance' : getAllData,
            'datenow' : getdateNow
        }
        return render(request, 'attendance/manager_page.html', context)

@login_required
def manager_member_detail(request, id):

    getAttendanceDetail = UserAttendance.objects.get(id = id)

    print(getAttendanceDetail.selfassstatus)

    getDate = timezone.localtime(getAttendanceDetail.created_at)
    
    data = {
        'selfass' : getAttendanceDetail.selfassstatus,
        'attendance' : getAttendanceDetail.attendance,
        'reasonNotPresent' : getAttendanceDetail.reasonNotPresent,
        'otherNotPresent' : getAttendanceDetail.otherNotPresent,
        'condition' : getAttendanceDetail.condition,
        'sickChoices' : getAttendanceDetail.sickChoices,
        'otherSicks' : getAttendanceDetail.otherSicks,
        'work_status' : getAttendanceDetail.work_status,
        'wfo_description' : getAttendanceDetail.wfo_description,
        'date_created' : getDate.strftime("%d-%m-%Y"),
        'time_created' : getDate.strftime("%H:%M"),
        
        'id' : getAttendanceDetail.id
    }

    return JsonResponse({'attendance':data}, status=200)

@login_required
def user_logout(request):
    try:
        del request.session['full_name']
        logout(request)
    except KeyError:
        pass

    return redirect('user_login')