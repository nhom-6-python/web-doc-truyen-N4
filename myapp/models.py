from django.db import models
from django.utils import timezone

# Create your models here.

class Truyen(models.Model):
	ten = models.CharField(max_length=255) # tên của bộ truyện
	theloai = models.TextField() # thẻ loại của truyện
	mota = models.TextField()	# mô tả của truyện
	tacgia = models.CharField(max_length=255) # tác giả bộ truyện
	luotthich = models.BigIntegerField(default=0) # số luợt yêu thích (theo dõi)
	anhbia = models.FileField(upload_to='anhbia/') # ảnh bìa truyện
	anhnen = models.FileField(upload_to='anhnen/') # ảnh nền của truyện
	@property 
	def luotxem(self): # phương thức lấy ra số lượt xem truyện
		return sum(x.luotxem for x in self.chap.all())

	@property
	def chapmoinhat(self): # phương thức lấy ra chap mới nhất của truyện
		return self.chap.order_by('-thoigiandang').first()
	@property 
	def sochap(self): # phương thức lấy ra số chap của 1 truyện
		return len(list(self.chap.all()))
	
class Chap(models.Model):
	stt = models.FloatField(default=0) # số thứ tự của chương
	ten = models.CharField(max_length=255) # tên chương
	luotxem = models.BigIntegerField(default=0) # lượt xem của chương 
	thoigiandang = models.DateTimeField(default=timezone.now) # thời gian chương được đăng
	truyen = models.ForeignKey(Truyen, on_delete=models.CASCADE, related_name='chap') #chương này thuộc truyện nào
	def formatted_time(self): # thuộc tính để format lại thời gian đăng đúng định dạng
		return self.thoigiandang.strftime('%d/%m/%Y %H:%M')	

class Trang(models.Model):
	anh = models.FileField(upload_to='anhchap/') # ảnh hiển thị cho trang đó
	chap = models.ForeignKey(Chap, on_delete=models.CASCADE, related_name='trang') # trang đó thuộc chap nào

class Thongbao(models.Model):
	theloai = models.CharField(max_length=255, default="Thông báo mới!!") #thể loại của thông báo
	noidung = models.CharField(max_length=255) # nội dung của thông báo
	chap = models.ForeignKey(Chap, on_delete=models.CASCADE, related_name='chap', default=None) # Thông báo của chap nào
class Nguoidung(models.Model):
    ten = models.CharField(max_length=255) # tên đăng nhập
    matkhau = models.CharField(max_length=255) # mật khẩu đăng nhập
    vaitro = models.CharField(max_length=255) # vai trò (nguoidoc) hoặc (nhomdich)
    yeuthich = models.ManyToManyField(Truyen, related_name='yeuthich', blank=True) # các truyện yêu thích(theo dõi)
    thongbao = models.ManyToManyField(Thongbao, related_name='thongbao', blank=True) # các thông báo được gửi đến
    truyendang = models.ManyToManyField(Truyen, related_name='truyendang', blank=True) # các truyện do người dùng đăng tải

    @property
    def sotruyendadang(self): # phương thức lấy ra số truyện đã đăng
        cnt = 0
        for x in self.truyendang.all():
            cnt += 1
        return cnt

    @property
    def luotxem(self): # phương thức lấy ra số lượt xem các truyện đã đăng
        return sum(x.luotxem for x in self.truyendang.all())
	
class Lichsu(models.Model):
	idchap = models.IntegerField() # id chương đã đọc
	idtruyen = models.IntegerField() # chương đó của truyện nào
	stt = models.FloatField(default=0) # stt chương đó 
	tentruyen = models.CharField(max_length=255) # tên chương đó
	anhbia = models.FileField(upload_to='anhbia/') # ảnh bìa truyện
	thoigiandoc = models.DateTimeField(default=timezone.now) # thời gian đọc chương đó
	nguoidoc = models.ForeignKey(Nguoidung, on_delete=models.CASCADE, related_name='lichsu') # người dùng nào đọc chương đó
	def formatted_time(self): # định dạng lại thời gian
		return self.thoigiandoc.strftime('%d/%m/%Y')	

class Theloai(models.Model):
	theloai = models.CharField(max_length=255) # thê loại là gì?