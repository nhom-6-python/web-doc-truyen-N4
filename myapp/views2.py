#Phuc
from django.shortcuts import render, redirect
from .models import Truyen, Chap, Trang, Thongbao, Nguoidung
from .forms import TruyenForm
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.utils import timezone
from django.db.models import Sum,Q, Value
from django.db.models.functions import Coalesce
from .views import get_nguoidung, checklogin

def list_thong_bao(request):
    if checklogin(request):
        nguoidung = get_nguoidung(request)
        print(nguoidung)
        return nguoidung.thongbao.all()
