from django.db import models

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
	
class Chap(models.Model):
	stt = models.FloatField(default=0)
	ten = models.CharField(max_length=255)
	luotxem = models.BigIntegerField(default=0)
	thoigiandang = models.DateTimeField(auto_now_add=True)
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
    lichsu = models.ManyToManyField(Truyen, related_name='lichsu', blank=True)
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

