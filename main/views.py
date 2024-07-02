from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from authapp.models import CustomUser
from django.shortcuts import get_object_or_404
from authapp.forms import CustomUserEditForm
from planning.models import Appointment

# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

@login_required
def home(request):
    user = request.user
    if user.roles == 'student':
        return render(request, 'home_student.html', {'user': user})
    elif user.roles == 'instructor':
        return render(request, 'home_instructor.html', {'user': user})
    else:
        return render(request, 'home.html', {'user': user})

@login_required
def account(request):
    user = request.user
    return render(request, 'account.html', {'user': user})


@login_required
def settings(request):
    current_user = request.user
    if current_user.roles == 'secretary':
        users = CustomUser.objects.filter(roles__in=['student', 'instructor'])
    else:
        users = CustomUser.objects.filter(roles__in=['student', 'instructor', 'secretary'])
    return render(request, 'setting.html', {'users': users})

@login_required
def delete_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(CustomUser, id=user_id)
        user.delete()
        return redirect('main:settings')
    else:    
        return redirect('main:settings')

@login_required
def update_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1 and password1 == password2:
                user.set_password(password1)
            if 'hours_paid' in request.POST and request.POST.get('hours_paid').isdigit():
                user.hours_paid += int(request.POST.get('hours_paid'))
            user.save()
            return redirect('main:settings')
    else:
        form = CustomUserEditForm(instance=user)
    return render(request, 'update_user.html', {'form': form, 'user': user})



@login_required
def student_list(request):
    if request.user.roles == 'instructor':
        appointments = Appointment.objects.filter(instructor=request.user)
        students_with_appointments = set(appointment.student for appointment in appointments)
        students = CustomUser.objects.filter(roles='student', id__in=[student.id for student in students_with_appointments])
        return render(request, 'student_list.html', {'students': students})
    elif request.user.roles == 'secretary' or request.user.roles == 'admin':
        students = CustomUser.objects.filter(roles='student')
        return render(request, 'student_list.html', {'students': students})
    else:
        return redirect('main:home')

@login_required
def student_details(request, student_id):
    user = get_object_or_404(CustomUser, id=student_id)
    if user.roles == 'student':
        appointments = Appointment.objects.filter(student=user)
    else:
        appointments = Appointment.objects.filter(instructor=user)
    return render(request, 'student_details.html', {'student': user, 'appointments': appointments})

@login_required
def instructor_list(request):
    instructors = CustomUser.objects.filter(roles='instructor')
    return render(request, 'instructor_list.html', {'instructors': instructors})


@login_required
def instructor_details(request, instructor_id):
    user = get_object_or_404(CustomUser, id=instructor_id)
    appointments = Appointment.objects.filter(instructor=user)
    return render(request, 'instructor_details.html', {'instructor': user, 'appointments': appointments})