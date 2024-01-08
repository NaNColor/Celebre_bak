from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.utils.http import urlunquote
from .models import *
from datetime import datetime, date, timedelta
import telegram # this is from python-telegram-bot package
from django.conf import settings
from django.views.decorators.gzip import gzip_page
 
#from asgiref.sync import sync_to_async
#@sync_to_async sync_to_async(thread_sensitive=False)
def post_event_on_telegram(message_html):
    telegram_settings = settings.TELEGRAM
    bot = telegram.Bot(token=telegram_settings['bot_token'])
    bot.send_message(chat_id="@%s" % telegram_settings['channel_name'],
                    text=message_html, parse_mode=telegram.ParseMode.HTML)

def add_schedule_2x2():
    stylists = Stylist.objects.all()
    for worker in stylists:
        if worker.work_style == 2:
            end_date = WorkSchedule.objects.filter(stylist = worker.pk).order_by('-day_of_work').first().day_of_work
            if (end_date is None) or (end_date > date.today() + timedelta(days=7)):
                continue
            end_date = end_date - timedelta(days=1)
            q = WorkSchedule.objects.filter(stylist = worker.pk).order_by('day_of_work').filter(day_of_work__gte = end_date)
            #выбираем даты большие предпоследней в записи, чтобы на сонове двух последних записанных днях делть вывод о следующем дне
            if q[1].is_work == q[0].is_work == True:
                new_work_schedule = WorkSchedule(stylist = Stylist(id = worker.pk),
                    day_of_work = q[1].day_of_work + timedelta(days=1), is_work = False)
            elif q[1].is_work == q[0].is_work == False:
                new_work_schedule = WorkSchedule(stylist = Stylist(id = worker.pk),
                    day_of_work = q[1].day_of_work + timedelta(days=1), is_work = True)
            else:
                new_work_schedule = WorkSchedule(stylist = Stylist(id = worker.pk),
                    day_of_work = q[1].day_of_work + timedelta(days=1), is_work = q[1].is_work)
            new_work_schedule.save()
    #post_event_on_telegram("Успешно добавлено расписание")

def add_blocks():
    end_date = WorkSchedule.objects.order_by('-day_of_work').first().day_of_work
    if end_date > date.today() + timedelta(days=7):
        return
    if not Blocks.objects.order_by('-date').first():
        begin_date = date.today()
    else:
        begin_date = Blocks.objects.order_by('-date').first().date

    times = Times.objects.all()
    stylists = Stylist.objects.all()
    if begin_date is None or begin_date < date.today():
        begin_date = date.today()
    if end_date is None or end_date < date.today():
        end_date = date.today()
    while begin_date != end_date:
        begin_date+= timedelta(days=1)
        for worker in stylists:
            q = WorkSchedule.objects.filter(stylist = worker.pk).filter(day_of_work = begin_date)
            if not q:
            	continue
            if q[0].is_work:
                for time in times:
                    Blocks.objects.create(time_id=time.id, date=begin_date, stylist=worker)
    #post_event_on_telegram("Успешно добавлены блоки расписания")

def del_schedule_2x2():
	WorkSchedule.objects.filter(day_of_work__lt = date.today() - timedelta(days=2)).delete()
def del_blocks():
	Blocks.objects.filter(date__lt=date.today()).delete()

@gzip_page
def register_steps(request):
	if request.method == 'POST':
		id_op = request.POST["option"]
		op = "Услуга: " + Option.objects.get(pk=id_op).name
		time = ""
		times = Times.objects.all()
		for t in times:
			try:
				if request.POST["time"+str(t.id)]:
					minute=str(t.time_clock.minute)
					if minute=="0":
						minute="00"
					time += " " + str(t.time_clock.hour) + ":" + minute
			except:
				pass
		if time == "":
			time = "Любое"
		post_event_on_telegram("Запрос на звонок!"+ "\n" +"<b>"+op+"</b>" + "\n" + "Время: "+ time  + "\n" + "Тел: " + request.POST["phone"])
		return redirect('success')
	else:
		options = Option.objects.all().order_by('price')
		times = Times.objects.all()
		return render(request, "register_steps.html",{ 'options':options, 'time':times})

class ops:
    def __init__(self,id_num, name, count_time_block, price):
        self.id = id_num
        self.name = name
        self.count_time_block = count_time_block
        self.price = price

@gzip_page
def register_write(request):
	error_flag = True
	if request.method == 'POST':
		time_beg = time(0,0)
		try:
			time_beg=Times.objects.get(id = request.POST["time"]).time_clock
		except:
			pass
		if time_beg == time(0,0):
			error_flag = True
		op = Option.objects.all().get(pk = int(request.POST["option-select"]))
		time_end = datetime.strptime(str(timedelta(hours=time_beg.hour, minutes=time_beg.minute) + \
		timedelta(hours=op.count_time_block.hour, minutes=op.count_time_block.minute)),"%H:%M:%S").time()
		day = datetime.strptime(request.POST["day-select"]+"."+str(date.today().year),"%d.%m.%Y").date()
		blocks = Blocks.objects.filter(date = day).filter(time__in = Times.objects.filter(time_clock__gte=time_beg).filter(time_clock__lt=time_end))
		try:
			patronymic = request.POST["patronymic"]
		except Exeption:
			patronymic = " "
		if request.POST["stylist-select"] == "0":
			st = WorkSchedule.objects.filter(day_of_work=day).filter(is_work = True)[0].stylist
		else:
			st = Stylist.objects.get(pk = int(request.POST["stylist-select"]))
		for block in blocks:
			if block.appointment != None:
				error_flag = True
		if not error_flag:
			ap = Appointment.objects.create(
				client_name=request.POST["name"], client_patronymic=patronymic, 
				client_phone=request.POST["phone"], appointment_date = day,
				appointment_beg_date=time_beg, appointment_end_date = time_end,
				option = op, stylist = st)
			for block in blocks:
				block.appointment = ap
				block.save(update_fields=["appointment"])
			post_event_on_telegram("Создана запись")
			return redirect('success')
	listop = []
	today = date.today()
	times = Times.objects.filter(time_clock__lt = datetime.strptime('17:00','%H:%M'))
	bloks = Blocks.objects.filter(date__gte = today).order_by('id')
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
		listop.append(ops(op.id,name, count, price))
	schedule = WorkSchedule.objects.filter(day_of_work__gte=today).filter(is_work = True)
	#data = list(set(schedule))
	days = []
	for day in schedule:
		days.append(day.day_of_work)
	days = list(set(days))
	days.sort()
	stylists = Stylist.objects.all()
	first_time = Times.objects.order_by('time_clock').first().id
	return render(request, "register_write.html",{ 'options':listop, 'time':times,'error_flag':error_flag,
	"today":today,"days":days,"stylists":stylists, "bloks":bloks,"first_time":first_time})
	
def register_start(request):
	if request.method == 'POST':
		try:
			a = request.POST["phone"]
			return redirect('register_steps')
		except Exception:
			pass
		return redirect('register_write')
	return render(request, "register.html")

def functions(request):
	return redirect('proxy_func')

def proxy_func(request):
	try:
		add_schedule_2x2()
		add_blocks()
		del_schedule_2x2()
		del_blocks()
	except Exception:
		post_event_on_telegram("Переодическое задание прошло не успешно")
	except SyntaxError:
		post_event_on_telegram("ошибка синтаксиса")
	return redirect('success')
    
def success(request):
    return render(request, "success.html")
