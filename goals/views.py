from django.shortcuts import render, redirect, get_object_or_404
from .models import LearningGoal, SingleTask
from django.db.models import Prefetch, Count
from django.contrib import messages
from .forms import CreateUserForm, CreateGoalForm, CreateSingleTask
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
    LearningGoals = request.user.learninggoal_set.prefetch_related(
        Prefetch('tasks', queryset=SingleTask.objects.filter(completed=False))).annotate(
        counter=Count('tasks')).order_by('-updated_at')
    context = {'LearningGoals': LearningGoals}
    return render(request, template_name, context)


@login_required(login_url='login')
def create_goal(request):
    if request.method == 'POST':
        form = CreateGoalForm(request.POST)
        user = request.user
        if form.is_valid():
            new_learning_goal = LearningGoal()
            new_learning_goal.name = form.cleaned_data['name']
            new_learning_goal.user = user
            new_learning_goal.save()
            print(new_learning_goal)
            return redirect('dashboard')
    form = CreateGoalForm()
    context = {'form' :form}
    return render(request, 'single_goal/create_goal.html', context)


@login_required(login_url='login')
def LearningGoalTasks(request, id):
    tasks = LearningGoal.objects.get(id=id).tasks.all().order_by('completed')
    form = CreateSingleTask()
    context = {'tasks': tasks, 'form': form}
    return render(request, 'single_goal/create_tasks.html', context)




# def updateOrder(request, pk):
#     order = Order.objects.get(id=pk)
#     form = OrderForm(instance=order)
#     print('ORDER:', order)
#     if request.method == 'POST':

#         form = OrderForm(request.POST, instance=order)
#         if form.is_valid():
#             form.save()
#             return redirect('/')

#     context = {'form': form}
#     return render(request, 'accounts/order_form.html', context)

