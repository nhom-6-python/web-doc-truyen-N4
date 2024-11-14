from django.contrib import admin
from .models import Truyen, Chap, Trang, Thongbao, Nguoidung, Lichsu, Theloai
# Register your models here.

class TruyenAdmin(admin.ModelAdmin):
	list_display = ("id", "ten", "theloai", "mota", "tacgia", "luotthich", "luotxem", 'anhbia', 'anhnen')

class ChapAdmin(admin.ModelAdmin):
	list_display = ("id",'stt', "ten", "luotxem", "thoigiandang", 'truyen')

class TrangAdmin(admin.ModelAdmin):
	list_display = ('id', 'anh', 'chap')

class ThongbaoAdmin(admin.ModelAdmin):
	list_display = ('id','theloai', 'noidung','chap')

class NguoidungAdmin(admin.ModelAdmin):
	list_display = ('id','ten', 'matkhau', 'vaitro', 'luotxem')
	filter_horizontal = ('yeuthich', 'thongbao', 'truyendang')

class LichsuAdmin(admin.ModelAdmin):
	list_display = ('id','idchap', 'idtruyen', 'stt', 'tentruyen', 'anhbia','thoigiandoc')

class TheloaiAdmin(admin.ModelAdmin):
	list_display = ('id', 'theloai')

admin.site.register(Truyen, TruyenAdmin)
admin.site.register(Chap, ChapAdmin)
admin.site.register(Trang, TrangAdmin)
admin.site.register(Thongbao, ThongbaoAdmin)
admin.site.register(Nguoidung, NguoidungAdmin)
admin.site.register(Lichsu, LichsuAdmin)
admin.site.register(Theloai, TheloaiAdmin)