from django.contrib import auth, messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.contenttypes.models import ContentType
from .filters import DataFilter
from .forms import *

from .models import *


# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('username')
        password = request.POST.get('password')
        phone = request.POST.get('username')
        User._meta.get_field('email')._unique = True
        # username verification

        if User.objects.filter(username=username).exists():
            user = auth.authenticate(username=username, password=password)
            # Email Verification

        elif User.objects.filter(email=email).exists():
            username = User.objects.get(email=email.lower()).username
            user = authenticate(username=username, password=password)

            # Forign key data collect from Phone model to User model

        elif Student.objects.filter(phone=phone).exists():
            username = Student.objects.get(phone=phone)
            user = auth.authenticate(username=username, password=password)

        else:
            messages.info(request, 'Enter valid username/email/Phone')
            return render(request, 'login.html')
        # authenticate

        if user is not None:

            auth.login(request, user)
            if user.groups.filter(name='Teacher').exists():
                return redirect('show_list')
            else:
                return redirect('show')
        else:
            messages.info(request, 'incorrect password.')

            return render(request, 'login.html')

    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('login')


def is_Teacher(user):
    return user.groups.filter(name='Teacher').exists()


def is_Student(user):
    return user.groups.filter(name='Student').exists()


@login_required(login_url='login')
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone = request.POST['phone']
        g_name = request.POST['g_name']
        if g_name == 'Student':
            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username Already Taken')
                    return render(request, 'register.html')
                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email Already Taken')
                    return render(request, 'register.html')
                elif Student.objects.filter(phone=phone).exists():
                    messages.info(request, 'PhoneNumber already taken')
                    return render(request, 'register.html')
                else:
                    user = User.objects.create_user(username=username, password=password1, email=email)
                    user.save()
                    phone = Student.objects.create(phone=phone, user=user)
                    phone.save()
                    my_admin_group = Group.objects.get_or_create(name='Student')
                    my_admin_group[0].user_set.add(user)
                    user.has_perm('Main_app.view_Student')
                    return render(request, 'login.html')

            else:
                messages.info(request, "Password didn't match")
                return render(request, 'register.html')
        elif g_name == 'Teacher':

            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username Already Taken')
                    return render(request, 'register.html')
                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email Already Taken')
                    return render(request, 'register.html')
                elif Student.objects.filter(phone=phone).exists():
                    messages.info(request, 'PhoneNumber already taken')
                    return render(request, 'register.html')
                else:
                    user = User.objects.create_user(username=username, password=password1, email=email)
                    user.save()
                    phone = Student.objects.create(phone=phone, user=user)
                    phone.save()
                    my_admin_group = Group.objects.get_or_create(name='Teacher')
                    my_admin_group[0].user_set.add(user)
                    user.has_perm('Main_app.change_Student')

                    content_type = ContentType.objects.get_for_model(Student)
                    permission = Permission.objects.get(codename='change_Student', content_type=content_type)
                    user.user_permissions.add(permission)
                    return render(request, 'login.html')

            else:
                messages.info(request, "Password didn't match")
                return render(request, 'register.html')
        else:
            messages.info(request, "Please select a Group")
            return render(request, 'register.html')

    else:
        return render(request, 'register.html')


def show(request):
    data = Student.objects.all()
    user = DataFilter(request.GET, queryset=data)
    data = user.qs

    return render(request, 'list.html', {'user': user, 'data': data})


@user_passes_test(is_Teacher)
def show_list(request):
    data = Student.objects.all()
    user = DataFilter(request.GET, queryset=data)
    data = user.qs
    is_Teacher = True
    return render(request, 'list.html', {'user': user, 'data': data, 'is_Teacher': is_Teacher})


@user_passes_test(is_Teacher)
def delete(request, id):
    user1 = Student.objects.get(pk=id)
    user = User.objects.get(username=user1.user.username, email=user1.user.email)

    user1.delete()
    user.delete()
    return redirect('show_list')


@user_passes_test(is_Teacher)
def update(request, id):
    user1 = Student.objects.get(pk=id)
    user = User.objects.get(username=user1.user.username, email=user1.user.email)

    confirm = False
    form = userform(request.POST or None, request.FILES or None, instance=user1)
    if form.is_valid():
        user1.father_name = form.cleaned_data['father_name']
        user1.mother_name = form.cleaned_data['mother_name']
        user1.phone = form.cleaned_data['phone']
        form.save()
    form = userform(request.POST or None, request.FILES or None, instance=user)
    if form.is_valid():
        username = form.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username Already Taken')
            user.username = form.cleaned_data['username']
            user.password = form.cleaned_data['password']
            form.save()

            return redirect('show_list')

    return render(request, 'update.html', {'form': form, 'confirm': confirm})
