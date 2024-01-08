from django.db import models
# Create your models here.
class Galery(models.Model):
    title = models.CharField(max_length=255)#имя файла
    image_path = models.ImageField(upload_to="images/%Y-%m/")
    time_create = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
class Counter(models.Model):
	date = models.DateField(auto_now_add=True)
	count = models.IntegerField(verbose_name ="Счетчик", default = 1)
	def __str__(self):
		view = self.date.strftime("%d.%m.%Y") +" : "+ str(self.count)
		return view