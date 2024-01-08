from django.shortcuts import render
from register.models import Stylist
# Create your views here.
def about(request):
	stylists = Stylist.objects.all()
	return render(request,'about.html',{'stylists': stylists})