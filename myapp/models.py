from django.db import models
from django.utils import timezone

# Create your models here.

class Truyen(models.Model):
	ten = models.CharField(max_length=255)
	theloai = models.TextField()
	mota = models.TextField()
	tacgia = models.CharField(max_length=255)
	luotthich = models.BigIntegerField(default=0)
	anhbia = models.FileField(upload_to='anhbia/')
	anhnen = models.FileField(upload_to='anhnen/')
	@property
	def luotxem(self):
		return sum(x.luotxem for x in self.chap.all())
	@property
	def chapmoinhat(self):
		return self.chap.order_by('-thoigiandang').first()
	@property
	def sochap(self):
		return len(list(self.chap.all()))
	
class Chap(models.Model):
	stt = models.FloatField(default=0)
	ten = models.CharField(max_length=255)
	luotxem = models.BigIntegerField(default=0)
	thoigiandang = models.DateTimeField(default=timezone.now)
	truyen = models.ForeignKey(Truyen, on_delete=models.CASCADE, related_name='chap')
	def formatted_time(self):
		return self.thoigiandang.strftime('%d/%m/%Y %H:%M')	

class Trang(models.Model):
	anh = models.FileField(upload_to='anhchap/')
	chap = models.ForeignKey(Chap, on_delete=models.CASCADE, related_name='trang')

class Thongbao(models.Model):
	theloai = models.CharField(max_length=255, default="Thông báo mới!!")
	noidung = models.CharField(max_length=255)

class Nguoidung(models.Model):

    ten = models.CharField(max_length=255)
    matkhau = models.CharField(max_length=255)
    # Sử dụng choices đúng cấu trúc
    vaitro = models.CharField(max_length=255)
    yeuthich = models.ManyToManyField(Truyen, related_name='yeuthich', blank=True)
    thongbao = models.ManyToManyField(Thongbao, related_name='thongbao', blank=True)
    truyendang = models.ManyToManyField(Truyen, related_name='truyendang', blank=True)

    @property
    def sotruyendadang(self):
        cnt = 0
        for x in self.truyendang.all():
            cnt += 1
        return cnt

    @property
    def luotxem(self):
        return sum(x.luotxem for x in self.truyendang.all())
	
class Lichsu(models.Model):
	#get link
	idchap = models.IntegerField()
	idtruyen = models.IntegerField()
	#display
	stt = models.FloatField(default=0)
	tentruyen = models.CharField(max_length=255)
	anhbia = models.FileField(upload_to='anhbia/')

	thoigiandoc = models.DateTimeField(default=timezone.now)
	nguoidoc = models.ForeignKey(Nguoidung, on_delete=models.CASCADE, related_name='lichsu')
	def formatted_time(self):
		return self.thoigiandoc.strftime('%d/%m/%Y')	

class Theloai(models.Model):
	theloai = models.CharField(max_length=255)