from django.shortcuts import render

# Create your views here.

def index(request):
    # Renders the home page
    return render(request, 'monitor/index.html')

def login(request):
    # Renders the login screen
    return render(request, 'monitor/login.html')
