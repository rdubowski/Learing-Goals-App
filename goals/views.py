from django.shortcuts import render, redirect, get_object_or_404
from .models import LearningGoal, SingleTask
from django.db.models import Prefetch, Count
from django.contrib import messages
from .forms import CreateUserForm, CreateGoalForm, SingleTaskForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy


def welcome_screen(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        context = {}
        return render(request, 'to_do_manager/hello_screen.html', context)


def register_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')

                messages.success(request, 'Account was created for '+username)

                return redirect('login')
            else:
                messages.info(request, 'Username OR password is incorrect')
        context = {'form': form}
        return render(request, 'to_do_manager/register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
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


def logout_page(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    template_name = 'to_do_manager/dashboard.html'
    LearningGoals = request.user.learninggoal_set.prefetch_related(
         Prefetch('tasks',
                  queryset=SingleTask.objects.filter(completed=False))
                                                                 ).annotate(
                  counter=Count('tasks')).order_by('-updated_at')
    paginator = Paginator(LearningGoals, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, template_name, context)


@login_required(login_url='login')
def dashboard_table(request):
    template_name = 'to_do_manager/dashboard-table-view.html'
    LearningGoals = request.user.learninggoal_set.prefetch_related(
         Prefetch('tasks',
                  queryset=SingleTask.objects.filter(completed=False))
                                                                 ).annotate(
                  counter=Count('tasks')).order_by('-updated_at')
    TasksAll = SingleTask.objects.all()
    TasksAller = TasksAll.count()
    TasksCompleted = TasksAll.filter(completed=True).count()
    TasksUncompleted = TasksAll.filter(completed=False).count()
    context = {'LearningGoals': LearningGoals,
               'TasksAll': TasksAller,
               'TasksCompleted': TasksCompleted,
               'TasksUncompleted': TasksUncompleted}
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
            return redirect('dashboard')
    form = CreateGoalForm()
    context = {'form': form}
    return render(request, 'single_goal/create_goal.html', context)


@login_required(login_url='login')
def delete_goal(request, pk):
    goal = get_object_or_404(LearningGoal, id=pk)
    if request.method == "POST":
        goal.delete()
        return redirect('dashboard')
    context = {'goal': goal}
    return render(request, 'single_goal/delete_goal.html', context)


@login_required(login_url='login')
def change_goal_name(request, pk):
    learning_goal = get_object_or_404(LearningGoal, id=pk)
    form = CreateGoalForm(request.POST or None, instance=learning_goal)
    if form.is_valid():
        form.save()
        return redirect('dashboard')
    context = {'form': form, 'learninggoal': learning_goal}
    return render(request, 'single_goal/change_goal_name.html', context)


@login_required(login_url='login')
def learning_goal_tasks(request, pk):
    learning_goal = get_object_or_404(LearningGoal, id=pk)
    if request.method == "POST":
        form = SingleTaskForm(request.POST)
        if form.is_valid():
            new_task = SingleTask()
            new_task.text = form.cleaned_data['text']
            new_task.learninggoal = learning_goal
            new_task.save()
            return JsonResponse({'task': model_to_dict(new_task)}, status=200)
        else:
            return redirect('task_list_url')
    else:
        form = SingleTaskForm()
        tasks = learning_goal.tasks.all()
        context = {'form': form,
                   'tasks': tasks,
                   'learning_goal': learning_goal}
        return render(request, 'single_goal/create_tasks.html', context)


@login_required(login_url='login')
def task_complete(request, id):
    if request.method == "POST":
        task = SingleTask.objects.get(id=id)
        task.completed = True
        task.save()
        return JsonResponse({'task': model_to_dict(task)}, status=200)


@login_required(login_url='login')
def task_delete(request, id):
    if request.method == "POST":
        task = SingleTask.objects.get(id=id)
        task.delete()
        return JsonResponse({'result': 'ok'}, status=200)


class UpdateUser(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'to_do_manager/update_profile.html'
    form_class = CreateUserForm

    def test_func(self):
        obj = self.get_object()
        return obj.pk == self.request.user.pk

    def get_success_url(self, **kwargs):         
        return reverse_lazy('dashboard')
