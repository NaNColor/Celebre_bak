from django.shortcuts import render
from register.models import Stylist, Portfolio
# Create your views here.
def portfolio(request):
	imgs = Portfolio.objects.all().order_by('time_create')
	stylists = Stylist.objects.all()
	return render(request,'portfolio.html',{'portfolio': imgs,"stylists":stylists})