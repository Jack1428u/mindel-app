# pylint: disable=E0401
# pylint:disable=E1101
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .models import Course, Unit, Matricula
from .forms import *
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    if request.user.is_authenticated and request.method == 'GET':
        return redirect('courses')
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password'],
                                            email=form.cleaned_data['email'],
                                            )
            login(request, user)
        else:
            return render(request, 'home.html', {
                'form': form,
            })
        return redirect('courses')
    else:
        form = UserForm()
        return render(request, 'home.html', {
            'form': form,
        })


def signIn(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
        except Exception as _:
            return render(request, 'home.html', {
                'LoginForm': AuthenticationForm,
                'error': 'The data should be completed',
            })
        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'LoginForm': AuthenticationForm,
                'error': 'The data do not match',
            })
        login(request, user)
        return redirect('courses')
    else:
        return render(request, 'signin.html', {
            'LoginForm': AuthenticationForm,
        })


@login_required
def SignOut(request):
    try:
        logout(request)
        return redirect('home')
    except Exception as _:
        return redirect('home')


@login_required
def view_courses(request):
    student = request.user
    try:
        courses = student.enrolled_courses.all()
        return render(request, 'courses.html', {
            'courses': courses,
        })
    except Exception as _:
        return render(request, 'courses.html', {
            'courses': courses,
        })


@login_required
def course_detail(request, course_id):
    # prefetch_related: Realiza un join a nivel de Python que permite traer las unidades (que contienen los recursos).
    course = get_object_or_404(
        Course.objects.prefetch_related('units__resources'), id=course_id)
    #units = course.units.all()
    return render(request, 'units.html', {
        'course': course,
    })


def enroll_course(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        course = get_object_or_404(Course, id=course_id)

        # Usamos get_or_create para evitar error 500 si ya existe la matrícula
        Matricula.objects.get_or_create(student=request.user, course=course)
        return redirect('courses')
    courses = Course.objects.all()
    return render(request, 'enroll_course.html', {
        'courses': courses,
    })
