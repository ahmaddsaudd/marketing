from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def home(request):
    return render(request, "home.html")

@csrf_exempt  # Use this decorator for testing purposes only
def process_form(request):
    print("processing form")
    if request.method == 'POST':
        domain = request.POST.get('domain')
        keyword = request.POST.get('keyword')

        print("Received domain:", domain)
        print("Received keyword:", keyword)

        return render(request, 'home.html')
    
    