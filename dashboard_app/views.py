from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home_view(request):
    
    return render(request, 'home/home_page.html')
    # return HttpResponse(':) بيرك الصفحة تنتضرك')