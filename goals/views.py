from django.shortcuts import render, redirect, get_object_or_404
from .models import LearningGoal, SingleTask
from django.db.models import Prefetch, Count
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.



def welcome_screen(request):
    context = {}
    return render(request, 'to_do_manager/hello_screen.html', context)


def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account was created for ' + username)

            return redirect('login')

    context = {'form': form}
    return render(request, 'to_do_manager/register.html', context)


def loginPage(request):
    
    if request.method == 'POST':
        print("cze")
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Username OR password is incorrect')
    context = {}
    return render(request, 'to_do_manager/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    template_name = 'to_do_manager/dashboard.html'
    LearningGoals = request.user.learninggoal_set.prefetch_related(Prefetch('tasks', queryset=SingleTask.objects.filter(completed=False))).annotate(counter=Count('tasks'))
    context = {'LearningGoals': LearningGoals}
    return render(request, template_name, context)

# LearningGoals = LearningGoal.objects.prefetch_related(Prefetch('tasks', queryset=SingleTask.objects.filter(completed=False))).annotate(counter=Count('tasks'))
