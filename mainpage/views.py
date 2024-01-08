from django.shortcuts import render
from django.http import HttpResponse
from .models import Galery, Counter
from register.models import Option
from datetime import time, timedelta, date
from django.views.decorators.gzip import gzip_page
from django.db.models import F

class ops:
    def __init__(self, name, count_time_block, price):
        self.name = name
        self.count_time_block = count_time_block
        self.price = price

@gzip_page
def index(request):
	buf_count = Galery.objects.count()
	if(Counter.objects.filter(date = date.today()).count() != 0):
		Counter.objects.filter(date = date.today()).update(count=F('count') + 1)
	else:
		Counter.objects.create(count = 1)
	if buf_count % 3 == 0:
		data = Galery.objects.all()
	elif buf_count % 3 == 1:
		data = Galery.objects.filter(pk__lt=buf_count)
	elif buf_count % 3 == 2:
		data = Galery.objects.filter(pk__lt=buf_count-1)
	listop = []
	options = Option.objects.all().order_by('price')
	for op in options:
		name = op.name
		hour = op.count_time_block.hour
		minute = op.count_time_block.minute
		count = ""
		if hour!=0:
			if(hour>1 and hour<5):
				count = str(hour)+" часа "
			elif(hour==1):
				count = str(hour)+" час "
			else:
				count = str(hour)+" часов "
		if minute != 0:
			count += str(minute) + " минут"
		price = "От " +str(op.price)+" руб."
		listop.append(ops(name, count, price))
	return render(request,'index.html',{'data': data, 'count': buf_count, 'options':listop})
