from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from attendance.models import UserAttendance
from account.models import UserProfile
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
import json

# Create your views here.
@login_required
def index(request):
    getUserId = UserProfile.objects.get(full_name = request.session['full_name'])
    try:
        getLatesAttend = UserAttendance.objects.filter(authors_id = getUserId.user_id).latest('id')
        def checkAttend():
            getdate = timezone.localtime(timezone.now()).strftime('%Y-%m-%d')
            if getdate in str(getLatesAttend.created_at):
                return 'SUDAH'
            else:
                return 'BELUM'

        context = {
            'attend' : True,
            'full_name' : request.session['full_name'],
            'attendance_status' : getLatesAttend.attendance_status,
            'selfassstatus' : getLatesAttend.selfassstatus,
            'working_location' : getLatesAttend.working_location,
            'wfo_time' : getLatesAttend.wfo_time,
            'condition' : getLatesAttend.condition,
            'sick_reason' : getLatesAttend.sick_reason,
            'date' : getLatesAttend.created_at,
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
    getdate = timezone.localtime(timezone.now()).strftime('%Y-%m-%d')
    getAllData = UserAttendance.objects.filter(created_at__date = getdate)

    getFullName = []
    for i in getAllData:
        getUserId = UserProfile.objects.get(user = i.authors)
        getSick = UserAttendance.objects.filter(authors_id = getUserId.user_id, attendance_status = 'Sakit')
        getIzin = UserAttendance.objects.filter(authors_id = getUserId.user_id, attendance_status = 'Izin')
        if getSick:
            getFullName.append(getUserId.full_name + '(Sakit)')
        elif getIzin:
            getFullName.append(getUserId.full_name + '(Izin)')
        else:
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

    getWfoCount = UserAttendance.objects.filter(authors_id = getUserId.user_id, attendance_status = 'WFO').count()
    getWfhCount = UserAttendance.objects.filter(authors_id = getUserId.user_id, attendance_status = 'WFH').count()
    getSakitCount = UserAttendance.objects.filter(authors_id = getUserId.user_id, attendance_status = 'Sakit').count()
    getIzinCount = UserAttendance.objects.filter(authors_id = getUserId.user_id, attendance_status = 'Izin').count()

    kehadiran = []
    kehadiran.append(getWfoCount+getWfhCount)
    kehadiran.append(getSakitCount+getIzinCount)

    context = {
        'full_name' : request.session['full_name'],
        'attend' : kehadiran,
        'condition' : kondisi
    }

    return JsonResponse({'attendance':context}, status=200)

@login_required
def my_attendance_list(request):
    getUserId = UserProfile.objects.get(full_name = request.session['full_name'])

    getListAttendance = UserAttendance.objects.filter(authors_id = getUserId.user_id).all().order_by('-created_at')

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
        'attendance_status' : getAttendanceDetail.attendance_status,
        'selfassstatus' : getAttendanceDetail.selfassstatus,
        'working_location' : getAttendanceDetail.working_location,
        'wfo_time' : getAttendanceDetail.wfo_time,
        'condition' : getAttendanceDetail.condition,
        'sick_reason' : getAttendanceDetail.sick_reason,
        'date_created' : getDate.strftime("%d-%m-%Y"),
        'time_created' : getDate.strftime("%H:%M"),
        'id' : getAttendanceDetail.id
    }

    return JsonResponse({'attendance':data}, status=200)

@login_required
def my_attendance_edit(request, id):
    
    if request.method == 'POST':
        
        attendance = UserAttendance.objects.get(id = id)

        attendance.attendance_status = request.POST.get('attendance_status')
        attendance.selfassstatus = request.POST.get('selfassstatus')
        attendance.working_location = request.POST.get('working_location')
        attendance.wfo_time = request.POST.get('wfo_time')
        attendance.condition = request.POST.get('condition')
        attendance.sick_reason = request.POST.get('sick_reason')
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

    getUserData = UserProfile.objects.get(full_name = request.session['full_name'])
    
    context = {
        'full_name' : request.session['full_name'],
        'user_status' : getUserData
    }
    return render(request, 'attendance/more.html', context)

@login_required
def add_attend(request):

    attendance = UserAttendance()

    attendance.attendance_status = request.POST.get('attendance_status')
    attendance.selfassstatus = request.POST.get('selfassstatus')
    attendance.working_location = request.POST.get('working_location')
    attendance.wfo_time = request.POST.get('wfo_time')
    attendance.condition = request.POST.get('condition')
    attendance.sick_reason = request.POST.get('sick_reason')
    attendance.authors = request.user

    attendance.save()

    messages.success(request, 'Berhasil tambah data!')
    return redirect('all_attendance')

@login_required
def add_edit_attend_post(request):
    if request.method == 'POST':
        attendance = UserAttendance()

        attendance.attendance_status = request.POST.get('attendance_status')
        attendance.selfassstatus = request.POST.get('selfassstatus')
        attendance.working_location = request.POST.get('working_location')
        attendance.wfo_time = request.POST.get('wfo_time')
        attendance.condition = request.POST.get('condition')
        attendance.sick_reason = request.POST.get('sick_reason')
        attendance.authors = request.user

        attendance.save()

        messages.success(request, 'Berhasil tambah data!')
        return redirect('all_attendance')

    else:
        getStatus = request.GET.get('status', '')
        try:
            if getStatus == 'WFO':
                getUserId = UserProfile.objects.get(full_name = request.session['full_name'])
                getLatesAttend = UserAttendance.objects.filter(authors_id = getUserId.user_id, attendance_status = 'WFO').latest('id')

                context = {
                    'attendance_status' : getLatesAttend.attendance_status,
                    'selfassstatus' : getLatesAttend.selfassstatus,
                    'working_location' : getLatesAttend.working_location,
                    'wfo_time' : getLatesAttend.wfo_time,
                    'condition' : getLatesAttend.condition,
                    'sick_reason' : getLatesAttend.sick_reason,
                }
                return JsonResponse({'attendance':context}, status=200)
            
            elif getStatus == 'WFH':
                getUserId = UserProfile.objects.get(full_name = request.session['full_name'])
                getLatesAttend = UserAttendance.objects.filter(authors_id = getUserId.user_id, attendance_status = 'WFH').latest('id')

                context = {
                    'attendance_status' : getLatesAttend.attendance_status,
                    'selfassstatus' : getLatesAttend.selfassstatus,
                    'working_location' : getLatesAttend.working_location,
                    'wfo_time' : getLatesAttend.wfo_time,
                    'condition' : getLatesAttend.condition,
                    'sick_reason' : getLatesAttend.sick_reason,
                }
                return JsonResponse({'attendance':context}, status=200)
            
        except UserAttendance.DoesNotExist:
            context = {
                'not_exist' : 'Data belum ada :( , Kamu dapat menambah data baru pada tombol "Manual"'
            }
            return JsonResponse({'attendance':context}, status=200)

@login_required()
def manager_page(request):

    getDate = request.GET.get('date', '')
    getdateNow = timezone.localtime(timezone.now()).strftime('%Y-%m-%d')

    if getDate == 'now':

        getSehatCondition = UserAttendance.objects.filter(condition = 'Sehat', created_at__date = getdateNow).count()
        getSakitCondition = UserAttendance.objects.filter(attendance_status = 'Sakit', created_at__date = getdateNow).count()
    
        kondisi = []

        kondisi.append(getSehatCondition)
        kondisi.append(getSakitCondition)

        getWfoCount = UserAttendance.objects.filter(attendance_status = 'WFO', created_at__date = getdateNow).count()
        getWfhCount = UserAttendance.objects.filter(attendance_status = 'WFH', created_at__date = getdateNow).count()
        getSakitCount = UserAttendance.objects.filter(attendance_status = 'Sakit', created_at__date = getdateNow).count()
        getIzinCount = UserAttendance.objects.filter(attendance_status = 'Izin', created_at__date = getdateNow).count()

        kehadiran = []
        kehadiran.append(getWfoCount+getWfhCount)
        kehadiran.append(getSakitCount+getIzinCount)
        
        getAuthor = UserAttendance.objects.filter(attendance_status = 'Sakit', created_at__date = getdateNow)
    
        getFullNameSakit = []
        for i in getAuthor:
            getFullNameByAuthor = UserProfile.objects.get(user = i.authors)
            getFullNameSakit.append(getFullNameByAuthor.full_name)

        getAllData = UserAttendance.objects.filter(created_at__date = getdateNow).order_by('-created_at')

        context = {
            'attend' : kehadiran,
            'condition' : kondisi,
            'sick_name' : getFullNameSakit,
            'attendance' : getAllData,
            'datenow' : getdateNow,
            'status_data' : 'DATA HARI INI'
        }
        return render(request, 'attendance/manager_page.html', context)

    elif getDate == 'all':

        getSehatCondition = UserAttendance.objects.filter(condition = 'Sehat').count()
        getSakitCondition = UserAttendance.objects.filter(attendance_status = 'Sakit').count()
    
        kondisi = []

        kondisi.append(getSehatCondition)
        kondisi.append(getSakitCondition)

        getWfoCount = UserAttendance.objects.filter(attendance_status = 'WFO').count()
        getWfhCount = UserAttendance.objects.filter(attendance_status = 'WFH').count()
        getSakitCount = UserAttendance.objects.filter(attendance_status = 'Sakit').count()
        getIzinCount = UserAttendance.objects.filter(attendance_status = 'Izin').count()

        kehadiran = []
        kehadiran.append(getWfoCount+getWfhCount)
        kehadiran.append(getSakitCount+getIzinCount)
        
        getAuthor = UserAttendance.objects.filter(attendance_status = 'Sakit', created_at__date = getdateNow)
    
        getFullNameSakit = []
        for i in getAuthor:
            getFullNameByAuthor = UserProfile.objects.get(user = i.authors)
            getFullNameSakit.append(getFullNameByAuthor.full_name)

        getAllData = UserAttendance.objects.all().order_by('-created_at')

        context = {
            'attend' : kehadiran,
            'condition' : kondisi,
            'sick_name' : getFullNameSakit,
            'attendance' : getAllData,
            'datenow' : getdateNow,
            'status_data' : 'SEMUA DATA'
        }
        return render(request, 'attendance/manager_page.html', context)

    else:

        getSehatCondition = UserAttendance.objects.filter(condition = 'Sehat', created_at__date = getDate).count()
        getSakitCondition = UserAttendance.objects.filter(attendance_status = 'Sakit', created_at__date = getDate).count()
    
        kondisi = []

        kondisi.append(getSehatCondition)
        kondisi.append(getSakitCondition)

        getWfoCount = UserAttendance.objects.filter(attendance_status = 'WFO', created_at__date = getDate).count()
        getWfhCount = UserAttendance.objects.filter(attendance_status = 'WFH', created_at__date = getDate).count()
        getSakitCount = UserAttendance.objects.filter(attendance_status = 'Sakit', created_at__date = getDate).count()
        getIzinCount = UserAttendance.objects.filter(attendance_status = 'Izin', created_at__date = getDate).count()

        kehadiran = []
        kehadiran.append(getWfoCount+getWfhCount)
        kehadiran.append(getSakitCount+getIzinCount)
        
        getAuthor = UserAttendance.objects.filter(attendance_status = 'Sakit', created_at__date = getdateNow)
    
        getFullNameSakit = []
        for i in getAuthor:
            getFullNameByAuthor = UserProfile.objects.get(user = i.authors)
            getFullNameSakit.append(getFullNameByAuthor.full_name)

        getAllData = UserAttendance.objects.filter(created_at__date = getDate).order_by('-created_at')

        context = {
            'attend' : kehadiran,
            'condition' : kondisi,
            'sick_name' : getFullNameSakit,
            'attendance' : getAllData,
            'datenow' : getdateNow,
            'status_data' : 'DATA ' + getDate
        }
        return render(request, 'attendance/manager_page.html', context)

@login_required
def manager_member_detail(request, id):

    getAttendanceDetail = UserAttendance.objects.get(id = id)

    getDate = timezone.localtime(getAttendanceDetail.created_at)

    getFullNameByAuthor = UserProfile.objects.get(user = getAttendanceDetail.authors)

    data = {
        'full_name' : getFullNameByAuthor.full_name,
        'attendance_status' : getAttendanceDetail.attendance_status,
        'selfassstatus' : getAttendanceDetail.selfassstatus,
        'working_location' : getAttendanceDetail.working_location,
        'wfo_time' : getAttendanceDetail.wfo_time,
        'condition' : getAttendanceDetail.condition,
        'sick_reason' : getAttendanceDetail.sick_reason,
        'date_created' : getDate.strftime("%d-%m-%Y"),
        'time_created' : getDate.strftime("%H:%M"),
        'id' : getAttendanceDetail.id
    }

    return JsonResponse({'attendance':data}, status=200)

@login_required
def admin_page(request):

    getUserData = UserProfile.objects.all()
    
    context = {
        'data' : getUserData
    }

    return render(request, 'attendance/admin_page.html', context)

@login_required
def admin_page_detail(request, id):
    if request.method == 'POST':
        id = request.POST.get('id')

        userStatus = UserProfile.objects.get(id = id)

        userStatus.is_user = request.POST.get('is_user').title()
        userStatus.is_manager = request.POST.get('is_manager').title()

        userStatus.save()
        return JsonResponse({'attendance':'berhasil'}, status=200)
    else :
        getUserData = UserProfile.objects.get(id = id)
        
        data = {
            'is_manager' : getUserData.is_manager,
            'is_user' : getUserData.is_user,
        }

        return JsonResponse({'attendance':data}, status=200)

@login_required
def admin_delete_member(request, id):

    users = UserProfile.objects.get(id = id)

    UserProfile.objects.get(id = id).delete()
    User.objects.get(username = users.user).delete()
    
    try:
        UserAttendance.objects.get(authors__username = users.user).delete()
    except UserAttendance.DoesNotExist:
        pass

    messages.success(request, 'Berhasil hapus data!')

    return redirect('admin_page')


@login_required
def user_logout(request):
    try:
        del request.session['full_name']
        logout(request)
    except KeyError:
        pass

    return redirect('user_login')