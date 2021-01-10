from django.shortcuts import render

# Create your views here.
def welcome_screen(request):
    context = {}
    return render(request, 'to_do_manager/hello_screen.html', context)


def dasboard(request):
    # all_todos = Todo.objects.all()
    # context = {'all_todos': all_todos}
    context = {}
    return render(request, 'to_do_manager/dashboard.html', context)


def login(request):
    context = {}
    return render(request, 'to_do_manager/login.html', context)
    
def register(request):
    context = {}
    return render(request, 'to_do_manager/register.html', context)
