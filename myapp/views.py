from django.shortcuts import render, redirect
from .models import Truyen, Chap, Trang, Thongbao, Nguoidung
from .forms import TruyenForm
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.utils import timezone
from django.db.models import Sum,Q, Value
from django.db.models.functions import Coalesce
# Create your views here.

def index(request):
	return redirect('home/')

# trang này là các hàm mà các view dùng chung với nhau

#lấy người dùng hiện tại
def get_nguoidung(request): 
	ten_nguoi_dung=request.session.get('nguoidung',None)
	print(ten_nguoi_dung)
	nguoidung=Nguoidung()
	nguoi_dungs= Nguoidung.objects.all()
	for x in nguoi_dungs:
		if x.ten==ten_nguoi_dung:
			nguoidung=x
			break
	return nguoidung	

# check dang nhap
def checklogin(request):
    ten_nguoidung = request.session.get('nguoidung', None)  # Kiểm tra session có chứa 'nguoidung'
    if ten_nguoidung:
        return True
    else:
        return False