from django.shortcuts import render

# Create your views here.
def welcome_screen(request):
    context = {}
    return render(request, 'to_do_manager/hello_screen.html', context)