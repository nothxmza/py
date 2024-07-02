from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Appointment
from authapp.models import CustomUser
from django.utils.dateparse import parse_date, parse_time
from django.contrib import messages
from django.http import HttpResponseForbidden
from datetime import datetime

@login_required
def appointment_list(request, user_id=None):
    user = request.user
    if user_id:
        user_to_filter = get_object_or_404(CustomUser, id=user_id)
    else:
        user_to_filter = user
    
    appointments = []

    if user.roles == 'student':
        appointments = Appointment.objects.filter(student=user_to_filter)
        return render(request, 'appointment_student_list.html', {'appointments': appointments})
    elif user.roles == 'instructor':
        appointments = Appointment.objects.filter(instructor=user_to_filter)
        return render(request, 'appointment_instructor_list.html', {'appointments': appointments})
    elif user.roles == 'secretary' or user.roles == 'admin':
        appointments = Appointment.objects.all()
        return render(request, 'appointment_secretary_list.html', {'appointments': appointments})
    return render(request, 'appointment_student_list.html', {'appointments': appointments})


@login_required
def add_appointment(request, user_id=None):
	if user_id:
		user = get_object_or_404(CustomUser, id=user_id)
	else:
		user = request.user

	if request.method == 'POST':
		if user.roles == 'instructor':
			student = get_object_or_404(CustomUser, id=request.POST.get('student'))
			instructor = user
		elif user.roles == 'student':
			instructor = get_object_or_404(CustomUser, id=request.POST.get('instructor'))
			student = user
		else:
			student = get_object_or_404(CustomUser, id=request.POST.get('student'))
			instructor = get_object_or_404(CustomUser, id=request.POST.get('instructor'))

		date = request.POST.get('date')
		timeStart = request.POST.get('timeStart')
		timeEnd = request.POST.get('timeEnd')
		location = request.POST.get('location')

		# Convertir les temps en datetime
		start_datetime = datetime.combine(datetime.now().date(), datetime.strptime(timeStart, '%H:%M').time())
		end_datetime = datetime.combine(datetime.now().date(), datetime.strptime(timeEnd, '%H:%M').time())

		appointment_duration = (end_datetime - start_datetime).total_seconds() / 3600

		total_hours_taken = student.hours_taken + appointment_duration

		if total_hours_taken > student.hours_paid:
			messages.error(request, "Impossible d'ajouter le rendez-vous. Les heures totales prises dépasseraient les heures payées.")
			return redirect('planning:add_appointment')

		appointment = Appointment(
			student=student,
			instructor=instructor,
			date=date,
			timeStart=start_datetime.time(),
			timeEnd=end_datetime.time(),
			location=location
		)
		appointment.save()

		student.hours_taken += appointment_duration
		student.save()

		return redirect('planning:appointment_list')
	else:
		user = request.user
		print(user.roles)
		if user.roles == 'instructor':
			students = CustomUser.objects.filter(roles='student')
			return render(request, 'add_appointment.html', {'students': students})
		elif user.roles == 'student':
			instructors = CustomUser.objects.filter(roles='instructor')
			return render(request, 'add_appointment.html', {'instructors': instructors})
		else:
			students = CustomUser.objects.filter(roles='student')
			instructors = CustomUser.objects.filter(roles='instructor')
			return render(request, 'add_appointment.html', {'instructors': instructors, 'students': students})


@login_required
def edit_appointment(request, pk):
	appointment = get_object_or_404(Appointment, id=pk)
	student = appointment.student
	start_datetime = datetime.combine(datetime.now().date(), appointment.timeStart)
	end_datetime = datetime.combine(datetime.now().date(), appointment.timeEnd)
	appointment_duration1 = (end_datetime - start_datetime).total_seconds() / 3600
	print(appointment.student.hours_paid)
	if request.method == 'POST':
		date = request.POST.get('date')
		timeStart = request.POST.get('timeStart')
		timeEnd = request.POST.get('timeEnd')
		location = request.POST.get('location')
		appointment.date = parse_date(date)
		appointment.timeStart = parse_time(timeStart)
		appointment.timeEnd = parse_time(timeEnd)
		appointment.location = location

		start_datetime = datetime.combine(datetime.now().date(), appointment.timeStart)
		end_datetime = datetime.combine(datetime.now().date(), appointment.timeEnd)
		appointment_duration2 = (end_datetime - start_datetime).total_seconds() / 3600

		if appointment_duration2 > appointment_duration1:
			student.hours_taken += appointment_duration2 - appointment_duration1
			total_hours_taken = student.hours_taken
			if total_hours_taken > student.hours_paid:
				messages.error(request, "Impossible d'ajouter le rendez-vous. Les heures totales prises dépasseraient les heures payées.")
				return render(request, 'edit_appointment.html', {'appointment': appointment, 'student': student})
		elif appointment_duration2 < appointment_duration1:
			student.hours_taken -= appointment_duration1 - appointment_duration2
			total_hours_taken = student.hours_taken
			if total_hours_taken > student.hours_paid:
				messages.error(request, "Impossible d'ajouter le rendez-vous. Les heures totales prises dépasseraient les heures payées.")
				return render(request, 'edit_appointment.html', {'appointment': appointment, 'student': student})
		
		student.save()
		appointment.save()
		return redirect('planning:appointment_list')
	else:
		return render(request, 'edit_appointment.html', {'appointment': appointment, 'student': student})

@login_required
def delete_appointment(request, pk):
	appointment = get_object_or_404(Appointment, id=pk)

	start_datetime = datetime.combine(datetime.now().date(), appointment.timeStart)
	end_datetime = datetime.combine(datetime.now().date(), appointment.timeEnd)

	appointment_duration = (end_datetime - start_datetime).total_seconds() / 3600
	appointment.student.hours_taken -= appointment_duration
	appointment.student.save()
	appointment.delete()
	return redirect('planning:appointment_list')